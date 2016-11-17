from app.store.database import Database

db = Database()

db.add_user('johndoe', first_name='John', last_name='Doe', email='johndoe@gmail.com')
db.add_user('janedoe', first_name='Jane', last_name='Doe', email='janedoe@gmail.com')
