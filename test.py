from unittest import TestCase
import unittest
from api import Request

class TestRequest(TestCase):
    def test_request_dict(self):
        get_recv = 'GET /search?hl=zh-CN&oq=1 HTTP/1.1\r\n\r\n' \
                'Host: www.sxt.cn\r\n' \
                'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0\r\n' \
                'Accept: */*\r\n' \
                'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\n' \
                'Accept-Encoding: gzip, deflate\r\n' \
                'Referer: http://www.sxt.cn/u/366/blog/77\r\n' \
                'Cookie: JSESSIONID=7BA1BFCDE8F8326D3D302DB208C48883\r\n\r\n' \
                ''
        post_recv = 'POST /search HTTP/1.1\r\n\r\n' \
                'Host: www.sxt.cn\r\n' \
                'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0\r\n' \
                'Accept: */*\r\n' \
                'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\n' \
                'Accept-Encoding: gzip, deflate\r\n' \
                'Referer: http://www.sxt.cn/u/366/blog/77\r\n' \
                'Cookie: JSESSIONID=7BA1BFCDE8F8326D3D302DB208C48883\r\n\r\n' \
                'hl=zh-CN&oq=1'

        get_request = Request(get_recv)
        post_request = Request(post_recv)

        assert get_request.method == 'GET'
        assert get_request.path == '/search'
        assert get_request.query == { 'hl':'zh-CN', 'oq':'1'}
        assert get_request.header == 'Host: www.sxt.cn\r\n' \
                'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0\r\n' \
                'Accept: */*\r\n' \
                'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\n' \
                'Accept-Encoding: gzip, deflate\r\n' \
                'Referer: http://www.sxt.cn/u/366/blog/77\r\n' \
                'Cookie: JSESSIONID=7BA1BFCDE8F8326D3D302DB208C48883'
        assert get_request.body == ''

        assert post_request.method == 'POST'
        assert post_request.path == '/search'
        assert post_request.query == {}
        assert post_request.header == 'Host: www.sxt.cn\r\n' \
                'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0\r\n' \
                'Accept: */*\r\n' \
                'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\n' \
                'Accept-Encoding: gzip, deflate\r\n' \
                'Referer: http://www.sxt.cn/u/366/blog/77\r\n' \
                'Cookie: JSESSIONID=7BA1BFCDE8F8326D3D302DB208C48883'
        assert post_request.body == 'hl=zh-CN&oq=1'


if __name__ == '__main__':
    unittest.main()