import os

def log(*args, **kwargs):
    print('log', *args, **kwargs)


class Request(object):
    def __init__(self, recv):
        self.recv_dic = self.__parse_recv(recv)

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


    @property
    def method(self):
        return self.recv_dic['method']

    @property
    def path(self):
        return self.recv_dic['path']

    @property
    def query(self):
        return self.recv_dic['query']

    @property
    def header(self):
        return self.recv_dic['header']

    @property
    def form(self):
        return self.recv_dic['form']


def error(code=404):
    e = {
        405: b'HTTP/1.x 405 Method Not Allowed\r\n\r\n<h1>Method Not Allowed</h1>',
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def render_template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().encode('utf-8')


def redirect(url):
    pass