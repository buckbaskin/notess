import unittest
from app import server

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.editor_url = '/docs'

    def tearDown(self):
        pass

    def test_docs(self):
        response = self.client.get(self.editor_url, query_string='user_name=testuser&note_id=583cd3e64855a87f80000000')
        self.assertEqual(response.status_code, 200)
