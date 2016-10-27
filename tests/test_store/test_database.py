import unittest

from app.store.database import Database

from nose.tools import nottest
from jsonschema import validate
from jsonschema.exceptions import ValidationError

USER_ID = '123adf89'
CLASS_ID = 'abcdefgh'
NOTE_ID = '12345'
TRANSCRIPT_ID = 'abcde'

def myValidate(self, loaded_json, schema):
    try:
        validate(loaded_json, schema)
    except ValidationError:
        self.fail()

class TestBasicDB(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def testDatabaseExists(self):
        self.assertNotEqual(self.db, None)

