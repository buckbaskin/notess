from app import server

import unittest

from nose.tools import ok_

class ExampleTest(unittest.TestCase):
    def setUp(self):
        self.app_client = server.test_client()

    def test_index(self):
        res = self.app_client.get('/')
        ok_(res.status_code == 200)
