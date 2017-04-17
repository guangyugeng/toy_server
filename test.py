from unittest import TestCase
import unittest
from utils import log, Response, Request, Cookie
from models import User

class TestUtils(TestCase):
    def test_request(self):
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
                'Cookie: user=xiaoming; version=1\r\n' \
                'Connection: close\r\n\r\n' \
                ''
        post_recv = 'POST /maps/api/geocode/json HTTP/1.1\r\n' \
                'Host: maps.google.com:80\r\n' \
                'User-Agent: search4.py (Foundations of Python Network Programming)\r\n' \
                'Cookie: user=xiaoming; version=1\r\n' \
                'Connection: close\r\n\r\n' \
                'address=cn&sensor=false'

        get_request = Request(get_recv)
        post_request = Request(post_recv)

        assert get_request.method == 'GET'
        assert get_request.path == '/maps/api/geocode/json'
        assert get_request.query == { 'address':'cn', 'sensor':'false'}
        # log(get_request.header)
        assert get_request.headers == { 'Host': 'maps.google.com:80',
                'User-Agent': 'search4.py (Foundations of Python Network Programming)',
                'Connection': 'close',
                'Cookie': 'user=xiaoming; version=1'}
        assert get_request.cookies == { 'user':'xiaoming', 'version':'1'}
        assert get_request.form == {}

        assert post_request.method == 'POST'
        assert post_request.path == '/maps/api/geocode/json'
        assert post_request.query == {}
        assert post_request.headers == { 'Host': 'maps.google.com:80',
                'User-Agent': 'search4.py (Foundations of Python Network Programming)',
                'Connection': 'close',
                'Cookie': 'user=xiaoming; version=1'}
        assert post_request.cookies == { 'user':'xiaoming', 'version':'1'}
        assert post_request.form == { 'address':'cn', 'sensor':'false'}

    def test_Cookie(self):
        cookie = Cookie()
        cookie.version = 1
        cookie.user = 'xiaoming'
        assert cookie.user == 'xiaoming'
        assert cookie.version == 1
        assert cookie.__str__() == "user=xiaoming;version=1"

    def test_response(self):
        response = Response()
        assert response.__dict__ == {'status_code':200,
                                     'status_text':'OK',
                                     'headers':{ 'Content-Type': 'text/html' },
                                     'body':'<h1>Hello</h1>'}
        assert response.__str__() == 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello</h1>'


class TestModels(TestCase):
    def test_Model(self):
        form = {
            'username':'testModel',
            'password':'111'
        }
        user = User(form)
        assert user.username == 'testModel'
        assert user.password == '111'
        user.save()
        user.all()
        user.delete()

    def test_User(self):
        form = {
            'username':'testUser',
            'password':'111'
        }
        user = User(form)
        assert user.valid_register() == True
        user.save()
        assert user.valid_login() == True
        user.delete()



if __name__ == '__main__':
    unittest.main()