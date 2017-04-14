from api import render_template

def response_index():
    header = b'HTTP/1.1 200 OK\r\nContent-Type: text/html'
    body = render_template('index.html')
    r = header + b'\r\n\r\n' + body
    return r
