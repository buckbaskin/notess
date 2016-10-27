import unittest
import app.knowledge.dbpedia.depedia as DBPedia


class TestDBPedia(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSearchKeyword_empty(self):
        queryResult = DBPedia.DBPediaAPI.search("blahblahblah")
        self.assertFalse(queryResult.has_results())
        self.assertTrue(queryResult.get_responses().__len__() == 0)
        self.assertEqual(queryResult.__str__(), "Error: No Result")
        self.assertEqual(queryResult.__repr__(), queryResult.__str__())

    def testSearchKeyword_oneResult(self):
        queryResult = DBPedia.DBPediaAPI.search("bigtable")
        self.assertTrue(queryResult.has_results())
        self.assertTrue(queryResult.get_first_description().__contains__("storage"))
        self.assertTrue(queryResult.get_responses().__len__() == 1)
        self.assertEqual(queryResult.__str__(), queryResult.get_first_description())
        self.assertEqual(queryResult.__repr__(), queryResult.__str__())

    def testSearchKeyword_manyResults(self):
        queryResult = DBPedia.DBPediaAPI.search("waterfall")
        self.assertTrue(queryResult.has_results())
        self.assertTrue(queryResult.get_first_description().__contains__("vertical drop"))
        self.assertTrue(queryResult.get_descriptions().__len__() > 1)
        self.assertTrue(queryResult.get_responses().__len__() > 1)
        self.assertEqual(queryResult.__str__(), queryResult.get_first_description())
        self.assertEqual(queryResult.__repr__(), queryResult.__str__())
