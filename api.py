import os

def log(*args, **kwargs):
    print('log', *args, **kwargs)


class Request(object):
    def __init__(self, recv):
        self.recv_dic = self.__parse_recv(recv)

    def __parse_recv(self, recv):
        method =  recv.split()[0]
        path_query =  recv.split()[1]
        path, query = self.__parse_path(path_query)
        header = recv.split('\r\n\r\n')[1]
        body = recv.split('\r\n\r\n')[2]

        d = dict(
            method=method,
            path=path,
            query=query,
            body=body,
            header=header,
        )

        return d

    def __parse_path(self, path_query):
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
    def body(self):
        return self.recv_dic['body']


def doit(fd):
    pass

def read_requesthdrs(request_head):
    pass

def parse_url(url, filename, cgi_args):
    pass

def serve_static(fd, filename, file_size):
    pass

def serve_dynamic(fd, filename, cgi_args):
    pass