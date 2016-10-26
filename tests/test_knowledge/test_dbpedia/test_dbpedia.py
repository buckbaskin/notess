import unittest
import app.knowledge.dbpedia.depedia as DBPedia


class TestDBPedia(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSearchKeyword(self):
        response = DBPedia.DBPediaAPI.search("blahblahblah")
        self.assertFalse(response.has_results())

