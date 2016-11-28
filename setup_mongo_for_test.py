from app.store.database import Database

import pymongo
from pymongo.errors import DuplicateKeyError

db = Database()

USERNAME = '1234567890'
CLASS_NAME = 'EECS393'
NOTE_NAME1 = 'First Note'
NOTE_NAME2 = 'Second Note'
NOTE_ID1 = '123456789012345678901231'
NOTE_ID2 = '123456789012345678901232'

try:
    db.add_user(USERNAME, first_name='John', last_name='Doe', email='johndoe@gmail.com')
    db.add_user('j123456789', first_name='Jane', last_name='Doe', email='janedoe@gmail.com')
    print('added two users')
except DuplicateKeyError:
    print('existing users')

try:
    db.add_class(USERNAME, CLASS_NAME)
    print('added one class')
except DuplicateKeyError:
    print('existing class')

try:
    db.add_note(USERNAME, CLASS_NAME, NOTE_NAME1)
    db.add_note(USERNAME, CLASS_NAME, NOTE_NAME2)
    print('added two notes')
except DuplicateKeyError:
    print('existing notes')

