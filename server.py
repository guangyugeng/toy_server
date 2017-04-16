# -*- coding: UTF-8 -*-

import socket
from request import Request
from route.view import view_dict, error
from utils import log


def response_for_url(request):
    path = request.path
    r = view_dict.get(path, error)
    # log(r.__name__)
    response = r(request)
    # log(response)
    return response.encode('utf-8')


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
            print('path1, ', path)

            r = response_for_url(request)

            connection.sendall(r)

            connection.close()


if __name__ == '__main__':
    config = dict(
        host=socket.gethostname(),
        port=11116,
    )
    run(**config)