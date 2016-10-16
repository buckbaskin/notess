from app import server

import unittest

USER_ID = '123adf89'
CLASS_ID = 'abcdefgh'

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

