# -*- coding: UTF-8 -*-

import socket
from socket import AF_INET, SOCK_STREAM
from utils import log

def send(port, host=socket.gethostname()):
    s = socket.socket(AF_INET, SOCK_STREAM)

    log(host)
    s.connect((host, port))

    http_request = 'GET / HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(host)

    request = http_request.encode('utf-8')

    s.send(request)

    response = b''

    while True:
        r = s.recv(1024)
        if len(r) == 0:
            break
        response += r

    print('响应', response.decode('utf-8'))

send(11111)