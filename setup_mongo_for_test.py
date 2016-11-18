from app.store.database import Database

db = Database()

db.add_user('1234567890', first_name='John', last_name='Doe', email='johndoe@gmail.com')
db.add_user('j123456789', first_name='Jane', last_name='Doe', email='janedoe@gmail.com')
