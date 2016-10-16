from app import server

import unittest

from nose.tools import nottest

USER_ID = '123adf89'
CLASS_ID = 'abcdefgh'
NOTE_ID = '12345'
TRANSCRIPT_ID = 'abcde'

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()

    def testOneUser(self):
        response = self.client.get('/v1/users/one?user_id=%s' % (USER_ID,))
        self.assertEqual(response.status_code, 200)

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

    def testAllClass(self):
        response = self.client.get('%s?user_id=%s' % (self.all_url, USER_ID,))
        self.assertEqual(response.status_code, 200)

    def testAllClassFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

class TestNotesAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.all_url = '/v1/note/all'
        self.class_url = '/v1/note/class'

    def testAllNotes(self):
        response = self.client.get('%s?user_id=%s' % (self.all_url, USER_ID,))
        self.assertEqual(response.status_code, 200)

    def testAllNotesFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

    def testOneClass(self):
        response = self.client.get('%s?user_id=%s&class_id=%s' % (self.class_url, USER_ID, CLASS_ID,))
        self.assertEqual(response.status_code, 200)

    def testOneClassFail(self):
        response = self.client.get('%s' % (self.class_url,))
        self.assertEqual(response.status_code, 400)

    def testOneClassFail2(self):
        response = self.client.get('%s?user_id=%s' % (self.class_url, USER_ID,))
        self.assertEqual(response.status_code, 400)

class TestTranscriptAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.all_url = '/v1/note/all'
        self.class_url = '/v1/note/class'

    def testAllNotes(self):
        response = self.client.get('%s?user_id=%s' % (self.all_url, USER_ID,))
        self.assertEqual(response.status_code, 200)

    def testAllNotesFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

    def testOneClass(self):
        response = self.client.get('%s?user_id=%s&class_id=%s' % (self.class_url, USER_ID, CLASS_ID,))
        self.assertEqual(response.status_code, 200)

    def testOneClassFail(self):
        response = self.client.get('%s' % (self.class_url,))
        self.assertEqual(response.status_code, 400)

    def testOneClassFail2(self):
        response = self.client.get('%s?user_id=%s' % (self.class_url, USER_ID,))
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
        response = self.client.get('%s?user_id=%s' % (self.all_url, USER_ID,))
        self.assertEqual(response.status_code, 200)

    def testAllKeywordsFail(self):
        response = self.client.get('%s' % (self.all_url,))
        self.assertEqual(response.status_code, 400)

    def testClassKeyword(self):
        response = self.client.get('%s?user_id=%s&class_id=%s' % (self.class_url, USER_ID, CLASS_ID,))
        self.assertEqual(response.status_code, 200)

    def testClassKeywordFail(self):
        response = self.client.get('%s' % (self.class_url,))
        self.assertEqual(response.status_code, 400)

    def testNoteKeyword(self):
        response = self.client.get('%s?user_id=%s&note_id=%s' % (self.note_url, USER_ID, NOTE_ID))
        self.assertEqual(response.status_code, 200)

    def testNoteKeywordFail(self):
        response = self.client.get('%s' % (self.note_url,))
        self.assertEqual(response.status_code, 400)

    def testTranscriptKeyword(self):
        response = self.client.get('%s?user_id=%s&transcript_id=%s' % (self.transcript_url, USER_ID, TRANSCRIPT_ID))
        self.assertEqual(response.status_code, 200)

    def testTranscriptKeywordsFail(self):
        response = self.client.get('%s' % (self.transcript_url,))
        self.assertEqual(response.status_code, 400)
