import functools

def log(*args, **kwargs):
    print('log', *args, **kwargs)


def render_template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().encode('utf-8')


def route_index(request):
    # log('route_index')
    return render_template('index.html')


def route_login(request):
    return render_template('login.html')


def route_register(request):
    return render_template('register.html')


view_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}

