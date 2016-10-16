from app import server

import unittest

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()

    def testOneUser(self):
        response = self.client.get('/v1/users/one?user_id=123adf89')
        self.assertEqual(response.status_code, 200)
