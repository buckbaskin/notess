from app import server
from app.user import api as user_api
from app.knowledge import api as knowledge_api

@server.route('/')
def hello():
    return 'Hello World'
