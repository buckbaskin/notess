from app.user import api
from app.knowledge import api

@server.route('/')
def hello():
    return 'Hello World'
