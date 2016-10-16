from flask import Flask
server = Flask(__name__)

@server.route('/')
def hello():
    return 'Hello World'

from app import api

if __name__ == '__main__':
    server.run()
