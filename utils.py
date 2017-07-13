import time


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


class Cookie(object):
    def __init__(self):
        self.id = None
        self.max_age = 'Session'
        self.version = 1

    def __str__(self):
        return 'id={};version={}'.format(self.id,self.version)


class Session(dict):
    pass


class Response(object):
    # __slots__ = []

    def __init__(self):
        self.status = '200 OK'
        self.headers = [ ('Content-Type', 'text/html') ]
        self.body = "<h1>Hello</h1>"

    def headers_format(self):
        s = ''
        for header in self.headers:
            s = s + '{}: {}\r\n'.format(*header)
        return s

    def __str__(self):
        return 'HTTP/1.x {} \r\n{}\r\n{}'.format(self.status,
                                                 self.headers_format(),
                                                 self.body)


def request_property(name, expected_type):

    @property
    def prop(self):
        if type(self._recv_dic[name]) == expected_type:
            return self._recv_dic[name]
        else:
            raise TypeError("request property type error")

    @prop.deleter
    def prop(self):
        raise AttributeError("Can't delete property")

    return prop


class Request(object):
    # __slots__ = []

    method = request_property('method', str)
    path = request_property('path', str)
    query = request_property('query', dict)
    query_str = request_property('query_str', str)
    headers = request_property('headers', dict)
    form = request_property('form', dict)
    cookies = request_property('cookies', dict)

    def __init__(self, recv):
        self.recv_dic = recv
        self.recv = recv

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
            self._recv_dic = self._parse_recv(value)

    # Deleter function (optional)
    @recv_dic.deleter
    def recv_dic(self):
        raise AttributeError("Can't delete recv_dic")

    def _parse_recv(self, recv):
        method =  recv.split()[0]
        path_query =  recv.split()[1]
        path, query, query_str = self._parse_url(path_query)
        header_body = recv.split('\r\n', 1)[1]
        headers = self._parse_header(header_body.split('\r\n\r\n')[0])
        cookies = self._parse_cookies(headers)
        # log(header_body,header)
        if len(header_body.split('\r\n\r\n')) == 1:
            form = {}
        else:
            form = self._parse_form(header_body.split('\r\n\r\n')[1])

        d = dict(
            method=method,
            path=path,
            query=query,
            query_str=query_str,
            form=form,
            headers=headers,
            cookies=cookies,
        )

        return d

    def _parse_url(self, path_query):
        index = path_query.find('?')
        if index == -1:
            return path_query, {}, ''
        else:
            path, query_string = path_query.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            return path, query, query_string

    def _parse_form(self, query):
        args = query.split('&')
        # log(args)
        if args == ['']:
            return {}
        else:
            form = {}
            for arg in args:
                k, v = arg.split('=')
                form[k] = v
            return form

    def _parse_header(self, query):
        args = query.split('\r\n')
        if args == ['']:
            return {}
        else:
            form = {}
            for arg in args:
                k, v = arg.split(': ')
                form[k] = v
            return form

    def _parse_cookies(self, headers):
        cookie = headers.get('Cookie', '')
        kvs = cookie.split('; ')
        log('cookie', kvs)
        cookies = {}
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                cookies[k] = v
        return cookies
