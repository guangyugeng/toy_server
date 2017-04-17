import functools
from utils import log
from models import User
from utils import Session, Cookie, Response
import random

session = Session()


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def error(code=404):
    e = {
        405: 'HTTP/1.x 405 Method Not Allowed\r\n\r\n<h1>Method Not Allowed</h1>',
        404: 'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, '')


def render_template(name, response):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        response.body = f.read()
        return response


def route_index(request):
    # log('route_index')
    r = Response()
    return render_template('index.html', r).__str__()


def route_login(request):
    form = request.form
    # headers = request.headers
    r = Response()
    r = render_template('login.html', r)
    if request.method == 'POST':
        u = User(form)
        if u.valid_login():
            r.body = r.body.replace('{{result}}', "login success")
            cookie_id = random_str()
            session['cookie'] = cookie_id
            cookie = Cookie()
            cookie.id = cookie_id
            r.headers['Set-Cookie'] = cookie.__str__()
        else:
            r.body = r.body.replace('{{result}}', "login fail")
    elif request.method == 'GET':
        r.body = r.body.replace('{{result}}', "")
    else:
        r = error(405)

    return r.__str__()


def route_register(request):
    form = request.form
    r = Response()
    r = render_template('register.html', r)

    if request.method == 'POST':
        u = User(form)
        if u.valid_register():
            u.save()
            r.body = r.body.replace('{{result}}', "register success")
        else:
            r.body = r.body.replace('{{result}}', "register fail")
    elif request.method == 'GET':
        r.body = r.body.replace('{{result}}', "")
    else:
        r = error(405)
    return r.__str__()


view_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}

