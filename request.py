import os


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def typed_property(name, expected_type):

    @property
    def prop(self):
        return self._recv_dic[name]

    @prop.deleter
    def prop(self):
        raise AttributeError("Can't delete property")

    return prop


class Request(object):
    # __slots__ = []

    method = typed_property('method', str)
    path = typed_property('path', str)
    query = typed_property('query', dict)
    header = typed_property('header', str)
    form = typed_property('form', dict)

    def __init__(self, recv):
        self.recv_dic = recv
        # self.method = self.recv_dic['method']
        # self.path = self.recv_dic['path']
        # self.query = self.recv_dic['query']
        # self.header = self.recv_dic['header']
        # self.form = self.recv_dic['form']

    # Getter function
    @property
    def recv_dic(self):
        return self._recv_dic

    # Setter function
    @recv_dic.setter
    def recv_dic(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected recv')
        else:
            self._recv_dic = self.__parse_recv(value)

    # Deleter function (optional)
    @recv_dic.deleter
    def recv_dic(self):
        raise AttributeError("Can't delete recv_dic")

    def __parse_recv(self, recv):
        method =  recv.split()[0]
        path_query =  recv.split()[1]
        path, query = self._parse_url(path_query)
        header_body = recv.split('\r\n', 1)[1]

        header = header_body.split('\r\n\r\n')[0]
        # log(header_body,header)
        if len(header_body.split('\r\n\r\n')) == 1:
            form = {}
        else:
            form = self._parse_form(header_body.split('\r\n\r\n')[1])

        d = dict(
            method=method,
            path=path,
            query=query,
            form=form,
            header=header,
        )

        return d

    def _parse_url(self, path_query):
        index = path_query.find('?')
        if index == -1:
            return path_query, {}
        else:
            path, query_string = path_query.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            return path, query

    def _parse_form(self, query):
        args = query.split('&')
        log(args)
        if args == ['']:
            return {}
        else:
            form = {}
            for arg in args:
                k, v = arg.split('=')
                form[k] = v
            return form


