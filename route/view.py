import functools
from utils import log
from models import User


def error(request, code=404):
    e = {
        405: 'HTTP/1.x 405 Method Not Allowed\r\n\r\n<h1>Method Not Allowed</h1>',
        404: 'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, '')


def render_template(name):
    path = 'templates/' + name
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    with open(path, 'r', encoding='utf-8') as f:
        return header + '\r\n' + f.read()


def route_index(request):
    # log('route_index')
    return render_template('index.html')


def route_login(request):
    form = request.form
    r = render_template('login.html')
    if request.method == 'POST':
        # username = form['username']
        # password = form['password']
        u = User(form)
        if u.valid_login():
            r = r.replace('{{result}}', "login success")
        else:
            r = r.replace('{{result}}', "login fail")
    elif request.method == 'GET':
        r = r.replace('{{result}}', "")
    else:
        r = error(405)
    return r


def route_register(request):
    form = request.form
    r = render_template('register.html')
    if request.method == 'POST':
        # username = form['username']
        # password = form['password']
        u = User(form)
        if u.valid_register():
            u.save()
            r = r.replace('{{result}}', "register success")
        else:
            r = r.replace('{{result}}', "register fail")
    elif request.method == 'GET':
        r = r.replace('{{result}}', "")
    else:
        r = error(405)
    return r


view_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}

