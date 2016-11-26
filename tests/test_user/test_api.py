from app import server
from app.user.api.schema import (
    user_schema, user_list,
    class_schema, class_list,
    note_schema, note_list,
    transcript_schema, transcript_list,
    keyword_schema, keyword_list)

import json
import unittest

from nose.tools import nottest
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from bson.objectid import ObjectId

import json

FACEBOOK_USER_ID = '1234567890'
USERNAME = FACEBOOK_USER_ID
CLASS_NAME = 'EECS393'
NOTE_NAME = 'Design Patterns for Practical Use'
NOTE_ID = ObjectId('123456789012345678901234')
TRANSCRIPT_ID = ObjectId('abcdef0123456789abcdef01')

def myValidate(self, loaded_json, schema):
    try:
        validate(loaded_json, schema)
    except ValidationError:
        self.fail()

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()

    def testCreateUser(self):
        data = {
            'password': 'SuperFancyPassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com'
        }
        username_info = {'FACEBOOK_USER_ID': FACEBOOK_USER_ID}
        data_str = json.dumps(data)
        headers = [('Content-type', 'application/json')]
        response = self.client.post('/v1/users/new?username=%(FACEBOOK_USER_ID)s' % username_info, data=data_str, headers=headers)

        self.assertEqual(response.status_code, 200)
        json_dict = json.loads(response.data.decode())
        self.assertEqual(json_dict['email'], data['email'])
        self.assertEqual(json_dict['last_name'], data['last_name'])
        self.assertEqual(json_dict['first_name'], data['first_name'])

    def testOneUser(self):
        response = self.client.get('/v1/users/one?username=%s' % (USERNAME,))
        self.assertEqual(response.status_code, 200)
        myValidate(self, json.loads(response.data.decode()), user_schema)

    def testOneUserFailPath(self):
        response = self.client.get('/v1/users/one')
        self.assertEqual(response.status_code, 400)

    def testOneUserFailPath2(self):
        response = self.client.post('/v1/users/one')
        self.assertEqual(response.status_code, 405)

class TestClassAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.all_url = '/v1/class/all'
        self.one_url = '/v1/class/one'
        self.new_url = '/v1/class/new'
        self.update_url = '/v1/class/update'

    def testOneClass(self):
        response = self.client.get('%s?username=%s&class_name=%s' % (self.one_url, USERNAME, CLASS_NAME,))
        if response.status_code != 200:
            print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def testAllClass(self):
        response = self.client.get('%s?username=%s' % (self.all_url, USERNAME,))
        self.assertEqual(response.status_code, 200)
        myValidate(self, json.loads(response.data.decode()), class_list)

    def testAllClassFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

    def testNewClass(self):
        response = self.client.post('%s?username=%s&class_name=%s' % (self.new_url, USERNAME, CLASS_NAME,), data={})
        if response.status_code != 200:
            print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def testNewClassWithData(self):
        data = {
            'metadata': 'metadata'
        }
        response = self.client.post('%s?username=%s&class_name=%s' % (self.new_url, USERNAME, CLASS_NAME,), data=data)
        if response.status_code != 200:
            print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def testUpdateClass(self):
        data = {
            'metadata': 'Set this as metadata'
        }
        response = self.client.post('%s?username=%s&class_name=%s' % (self.update_url, USERNAME, CLASS_NAME,), data=data)
        if response.status_code != 200:
            print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def testUpdateClassNoData(self):
        data = {}
        response = self.client.post('%s?username=%s&class_name=%s' % (self.update_url, USERNAME, CLASS_NAME,), data=data)
        if response.status_code != 200:
            print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

class TestNotesAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.all_url = '/v1/note/all'
        self.class_url = '/v1/note/class'
        self.update_url = '/v1/note/update'
        self.new_url = '/v1/note/new'

    def testNewNote(self):
        data = {
            'class_name': CLASS_NAME,
            'note_name': NOTE_NAME
        }
        data = json.dumps(data)
        headers = [('Content-type', 'application/json')]
        response = self.client.post('%s?username=%s' % (self.new_url, USERNAME,), data=data, headers=headers)
        if response.status_code != 200:
            print(response.data)
        self.assertEqual(response.status_code, 200)

    def testNewNoteEmpty(self):
        data = {}
        response = self.client.post('%s?username=%s' % (self.new_url, USERNAME,), data=data)
        self.assertEqual(response.status_code, 400)

    def testUpdateNote(self):
        data = {
            'note_content': 'I have a fancy name'
        }
        data = json.dumps(data)
        headers = [('Content-type', 'application/json')]
        response = self.client.post('%s?username=%s&note_id=%s' % (self.update_url, USERNAME, NOTE_ID,), data=data, headers=headers)
        if response.status_code != 200:
            print(response.data)
        self.assertEqual(response.status_code, 200)

    def testUpdateNoteEmpty(self):
        data = {}
        response = self.client.post('%s?username=%s' % (self.update_url, USERNAME,), data=data)
        self.assertEqual(response.status_code, 400)

    def testAllNotes(self):
        response = self.client.get('%s?username=%s' % (self.all_url, USERNAME,))
        self.assertEqual(response.status_code, 200)
        myValidate(self, json.loads(response.data.decode()), note_list)

    def testAllNotesFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

    def testOneClass(self):
        response = self.client.get('%s?username=%s&class_name=%s' % (self.class_url, USERNAME, CLASS_NAME,))
        self.assertEqual(response.status_code, 200)
        myValidate(self, json.loads(response.data.decode()), note_list)

    def testOneClassFail(self):
        response = self.client.get('%s' % (self.class_url,))
        self.assertEqual(response.status_code, 400)

    def testOneClassFail2(self):
        response = self.client.get('%s?username=%s' % (self.class_url, USERNAME,))
        self.assertEqual(response.status_code, 400)

class TestTranscriptAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.all_url = '/v1/transcript/all'
        self.class_url = '/v1/transcript/class'
        self.note_url = '/v1/transcript/note'

    def testAllTranscripts(self):
        response = self.client.get('%s?username=%s' % (self.all_url, USERNAME,))
        self.assertEqual(response.status_code, 200)
        myValidate(self, json.loads(response.data.decode()), transcript_list)

    def testAllNotesFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

@nottest
def generate_test_keyword_variant(variant: str, getstr: str, get: bool = True, status: int = 200):
    if get or True:
        def inner_func(self):
            response = self.client.get(getstr)
            self.assertEqual(response.status_code, status)
        inner_func.__name__ = 'test_%s_keywords' % (variant,)
        inner_func.__test__ = True
        return inner_func

class TestKeywordAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.all_url = '/v1/keyword/all'
        self.class_url = '/v1/keyword/class'
        self.note_url = '/v1/keyword/note'
        self.transcript_url = '/v1/keyword/transcript'

    def testAllKeywords(self):
        response = self.client.get('%s?username=%s' % (self.all_url, USERNAME,))
        self.assertEqual(response.status_code, 200)

    def testAllKeywordsFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

    def testClassKeyword(self):
        response = self.client.get('%s?username=%s&class_name=%s' % (self.class_url, USERNAME, CLASS_NAME,))
        self.assertEqual(response.status_code, 200)

    def testClassKeywordFail(self):
        response = self.client.get('%s' % (self.class_url,))
        self.assertEqual(response.status_code, 400)

    def testNoteKeyword(self):
        response = self.client.get('%s?username=%s&note_id=%s' % (self.note_url, USERNAME, NOTE_ID))
        self.assertEqual(response.status_code, 200)

    def testNoteKeywordFail(self):
        response = self.client.get('%s' % (self.note_url,))
        self.assertEqual(response.status_code, 400)

    def testTranscriptKeyword(self):
        response = self.client.get('%s?username=%s&transcript_id=%s' % (self.transcript_url, USERNAME, TRANSCRIPT_ID))
        self.assertEqual(response.status_code, 200)

    def testTranscriptKeywordsFail(self):
        response = self.client.get('%s' % (self.transcript_url,))
        self.assertEqual(response.status_code, 400)
