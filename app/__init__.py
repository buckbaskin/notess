from flask import Flask
server = Flask(__name__, static_folder='../static', template_folder='../templates')

from app import api

if __name__ == '__main__':
    server.run()
