from wsgiref.simple_server import make_server
from jinja2 import Environment, FileSystemLoader

# def application(env, start_response):
#     headers = [('Content-Type', 'text/plain')]
#     start_response('200 OK', headers)
#     return ['El servidor se ejecutó correctamente'.encode('latin-1')]

# HTML = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Servidor wsgiref.simple_server</title>
#     </head>
#     <body>
#         <h1>El servidor se ejecutó correctamente</h1>
#     </body>
# </html>
# """


# def application(env, start_response):
#     headers = [('Content-Type', 'text/html')]
#     start_response('200 OK', headers)
#     return [bytes(HTML, 'latin-1')]


def application(env, start_response):
    headers = [('Content-Type', 'text/html')]
    start_response('200 OK', headers)
    
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    html = template.render({
        'title': 'Servidor wsgiref.simple_server',
        'name': 'Batman',
    })
    
    return [bytes(html, 'latin-1')]


server = make_server('localhost', 80, application)
server.serve_forever()
