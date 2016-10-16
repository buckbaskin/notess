from app import server

import unittest

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()

    def testOne(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
