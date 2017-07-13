# -*- coding: UTF-8 -*-
from wsgiref import simple_server
import socket
from utils import Request, Response
from route.view import view_dict, error
from utils import log
from io import StringIO
import sys


def response_for_url(request):
    path = request.path
    route = view_dict.get(path, error)
    # log(r.__name__)
    response = route(request)
    # log(response)
    return response.encode('utf-8')


class WSGIServer(object):
    request_queue_size = 1

    def __init__(self, server_address):
        # 创建一个监听的套接字
        self.listen_socket = listen_socket = socket.socket()
        ### 允许复用同一地址
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ### 绑定地址
        listen_socket.bind(server_address)
        ### 激活套接字
        listen_socket.listen(self.request_queue_size)
        ### 获取主机的名称及端口
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        ### 返回由 Web 框架/应用设定的响应头部字段
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            ### 获取新的客户端连接
            self.client_connection, client_address = listen_socket.accept()
            ### 处理一条请求后关闭连接，然后循环等待另一个连接建立
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024).decode('utf-8')
        self.request = Request(request_data)
        env = self.get_environ()
        body = self.application(env, self.start_response)
        self.finish_response(body)


    def get_environ(self):
        env = {}
        ### WSGI 必需变量
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        ### CGI 必需变量
        env['REQUEST_METHOD']    = self.request.method    # GET
        env['PATH_INFO']         = self.request.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        env['QUERY_STRING']      = self.request.query
        return env

    def start_response(self, status, response_headers, exc_info=None):
        ### 添加必要的服务器头部字段
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        ### 为了遵循 WSGI 协议，start_response 函数必须返回一个 'write'
        ### 可调用对象（返回值.write 可以作为函数调用）。为了简便，我们
        ### 在这里无视这个细节。
        ### return self.finish_response

    def finish_response(self, body):
        try:
            response = Response()
            status, response_headers = self.headers_set
            response.status = status
            response.headers = response_headers
            response.body = body
            self.client_connection.sendall(response.__str__().encode('utf-8'))
        finally:
            self.client_connection.close()


SERVER_ADDRESS = (HOST, PORT) = '', 8888

def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    httpd.serve_forever()

