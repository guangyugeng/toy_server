# -*- coding: UTF-8 -*-

import socket
from api import *


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def run(host=socket.gethostname(), port=12345):

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

            response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello!'

            if path == '/':
                print(response)
                r = response
            else:
                r = b'404 NOT FOUND'
            connection.sendall(r)

            connection.close()



if __name__ == '__main__':
    config = dict(
        host=socket.gethostname(),
        port=12345,
    )
    run(**config)