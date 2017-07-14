# from route.view import view_dict, error

import functools
from utils import log
from models import User
from utils import Session, Cookie, Response, Request
import random

session = Session()


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def route_404_error(request):
    r = Response()
    r.status = '404 NOT FOUND'
    r.body = '<h1>NOT FOUND</h1>'
    return r


def route_405_error(request):
    r = Response()
    r.status = '405 Method Not Allowed'
    r.body = '<h1>Method Not Allowed</h1>'
    return r


def render_template(name, response):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        response.body = f.read()
        return response


def route_index(request):
    r = Response()
    return render_template('index.html', r)


def route_login(request):
    form = request.form
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
            r.headers.append(('Set-Cookie', cookie.__str__()))
        else:
            r.body = r.body.replace('{{result}}', "login fail")
    elif request.method == 'GET':
        r.body = r.body.replace('{{result}}', "")
    else:
        r = route_405_error(request)

    return r


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
        r = route_405_error(request)
    return r


view_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}


def app(environ, start_response):
    route = view_dict.get(environ['PATH_INFO'], route_404_error)
    request = Request(environ['wsgi.input'].read())
    response = route(request)
    start_response(response.status, response.headers)
    return [response.body.encode('utf-8')]