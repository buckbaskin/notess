from app.store.database import Database

db = Database()

USER_ID = '1234567890'
CLASS_NAME = 'EECS393'

db.add_user(USER_ID, first_name='John', last_name='Doe', email='johndoe@gmail.com')
db.add_user('j123456789', first_name='Jane', last_name='Doe', email='janedoe@gmail.com')

db.add_class(USER_ID, CLASS_NAME)
