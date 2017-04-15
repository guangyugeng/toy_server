import functools

def log(*args, **kwargs):
    print('log', *args, **kwargs)


def error(request, code=404):
    e = {
        405: b'HTTP/1.x 405 Method Not Allowed\r\n\r\n<h1>Method Not Allowed</h1>',
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


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
        username = form['username']
        password = form['password']
        log(username, password)
        r = r.replace('{{success}}')
        return r
    elif request.method == 'GET':
        return r
    else:
        return error(405)


def route_register(request):
    return render_template('register.html')


view_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}

