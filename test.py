from unittest import TestCase
import unittest
from core import Request


def log(*args, **kwargs):
    print('log', *args, **kwargs)


class TestRequest(TestCase):
    def test_request_dict(self):
        """\
GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
Host: maps.google.com:80\r\n\
User-Agent: search4.py (Foundations of Python Network Programming)\r\n\
Connection: close\r\n\
\r\n\
"""
        get_recv = 'GET /maps/api/geocode/json?address=cn&sensor=false HTTP/1.1\r\n' \
                'Host: maps.google.com:80\r\n' \
                'User-Agent: search4.py (Foundations of Python Network Programming)\r\n' \
                'Connection: close\r\n\r\n' \
                ''
        post_recv = 'POST /maps/api/geocode/json HTTP/1.1\r\n' \
                'Host: maps.google.com:80\r\n' \
                'User-Agent: search4.py (Foundations of Python Network Programming)\r\n' \
                'Connection: close\r\n\r\n' \
                'address=cn&sensor=false'

        get_request = Request(get_recv)
        post_request = Request(post_recv)

        assert get_request.method == 'GET'
        assert get_request.path == '/maps/api/geocode/json'
        assert get_request.query == { 'address':'cn', 'sensor':'false'}
        log(get_request.header)
        assert get_request.header == 'Host: maps.google.com:80\r\n' \
                'User-Agent: search4.py (Foundations of Python Network Programming)\r\n' \
                'Connection: close'
        assert get_request.form == {}

        assert post_request.method == 'POST'
        assert post_request.path == '/maps/api/geocode/json'
        assert post_request.query == {}
        assert post_request.header == 'Host: maps.google.com:80\r\n' \
                'User-Agent: search4.py (Foundations of Python Network Programming)\r\n' \
                'Connection: close'
        assert post_request.form == { 'address':'cn', 'sensor':'false'}

if __name__ == '__main__':
    unittest.main()