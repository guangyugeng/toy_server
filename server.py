# -*- coding: UTF-8 -*-

import socket
from request import Request
from route.view import view_dict



def log(*args, **kwargs):
    print('log', *args, **kwargs)


def error(request, code=404):
    e = {
        405: b'HTTP/1.x 405 Method Not Allowed\r\n\r\n<h1>Method Not Allowed</h1>',
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_url(request):
    path = request.path
    r = view_dict.get(path, error)
    response = r(request)
    return response


def run(host=socket.gethostname(), port=10000):

    with socket.socket() as s:
        s.bind((host, port))

        while True:
            log('1')
            s.listen(5)
            connection, address = s.accept()
            log('2')
            recv = connection.recv(1024)
            if len(recv) == 0:
                continue

            request = Request(recv.decode('utf-8'))

            path = request.path
            print('path1, ', path == '/')

            r = response_for_url(request)

            connection.sendall(r)

            connection.close()


if __name__ == '__main__':
    config = dict(
        host=socket.gethostname(),
        port=11114,
    )
    run(**config)