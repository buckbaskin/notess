import unittest
import json
import app.knowledge.dbpedia.dbpedia as DBPedia
from unittest.mock import MagicMock

class TestDBPedia(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSearchKeyword_empty(self):
        mockPedia = MagicMock()
        mock_keyword = "blahblahblah"
        mock_return = {'results': []}
        mock_return_json = json.dumps(mock_return)
        mock_result = DBPedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mockPedia.search.return_value = mock_result
        queryResult = mockPedia.search("blahblahblah")
        self.assertFalse(queryResult.has_results())
        self.assertTrue(queryResult.get_responses().__len__() == 0)
        self.assertEqual(queryResult.__str__(), "Error: No Result")
        self.assertEqual(queryResult.__repr__(), queryResult.__str__())

    def testSearchKeyword_oneResult(self):
        mockpedia = MagicMock()
        mock_keyword = "bigtable"
        mock_return = {'results': [{'description': 'mock_answer1'}]}
        mock_return_json = json.dumps(mock_return)
        mock_result = DBPedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mockpedia.search.return_value = mock_result
        queryResult = mockpedia.search("bigtable")
        self.assertTrue(queryResult.has_results())
        self.assertTrue(queryResult.get_first_description().__contains__("mock_answer1"))
        self.assertTrue(queryResult.get_responses().__len__() == 1)
        self.assertEqual(queryResult.__str__(), queryResult.get_first_description())
        self.assertEqual(queryResult.__repr__(), queryResult.__str__())

    def testSearchKeyword_manyResults(self):
        mockpedia = MagicMock()
        mock_keyword = "waterfall"
        mock_return = {'results': [{'description': 'mock_answerA'}, {'description': 'mock_answer2'}]}
        mock_return_json = json.dumps(mock_return)
        mock_result = DBPedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mockpedia.search.return_value = mock_result
        queryResult = mockpedia.search("waterfall")
        self.assertTrue(queryResult.has_results())
        self.assertTrue(queryResult.get_first_description().__contains__("mock_answerA"))
        self.assertTrue(queryResult.get_descriptions().__len__() > 1)
        self.assertTrue(queryResult.get_responses().__len__() > 1)
        self.assertEqual(queryResult.__str__(), queryResult.get_first_description())
        self.assertEqual(queryResult.__repr__(), queryResult.__str__())
