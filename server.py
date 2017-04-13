# -*- coding: UTF-8 -*-

import socket

host = socket.gethostname()
port = 12343

s = socket.socket()
s.bind((host, port))

def read_from_file(filename):
    with open(filename, 'rb') as f:
        return f.read()


while True:

    s.listen(5)
    connection, address = s.accept()

    request = connection.recv(1024)

    request = request.decode('utf-8')
    if len(request) == 0:
        continue

    line = request.split('\n')[0]
    print('line', line)
    path = line.split()[1]
    print('path1, ', path == '/')

    normal_response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello Gua!'

    if path == '/':
        print(normal_response)
        r = normal_response
    else:
        r = b'404 NOT FOUND'
    connection.sendall(r)

    connection.close()
