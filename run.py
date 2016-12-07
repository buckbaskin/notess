from app import server

if __name__ == '__main__':
    server.config['SERVER_NAME'] = 'localhost:8000'
    print('Hello World')
    server.run()
