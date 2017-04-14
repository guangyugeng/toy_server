# -*- coding: UTF-8 -*-

import socket
from api import *


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def response_index():
    return b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello!'


def error(code=404):
    e = {
        405: b'HTTP/1.x 405 Method Not Allowed\r\n\r\n<h1>Method Not Allowed</h1>',
    }
    return e.get(code, b'')


def get_response(path):
    if path == '/':
        r = response_index()
    elif path == '':
        r = b''
    else:
        r = b'404 NOT FOUND'


def post_response(path, form):
    if path == '/':
        r = response_index()
    elif path == '':
        r = b''
    else:
        r = b'404 NOT FOUND'


def response_for_url(request):
    method = request.method
    path = request.path
    form = request.form
    if method == 'GET':
        return get_response(path)
    elif method == 'POST':
        return post_response(path, form)
    else:
        return error(405)



def run(host=socket.gethostname(), port=10000):

    with socket.socket() as s:
        s.bind((host, port))

        while True:

            s.listen(5)
            connection, address = s.accept()

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
        port=10000,
    )
    run(**config)