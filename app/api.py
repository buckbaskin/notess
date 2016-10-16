from app import server
from app.user import api as user_api
from app.knowledge import api as knowledge_api

from flask import render_template

@server.route('/')
def hello():
    return render_template('index.html')