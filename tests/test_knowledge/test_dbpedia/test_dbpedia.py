import unittest
import json
import requests
import app.knowledge.dbpedia.dbpedia as DBPedia
from unittest.mock import Mock, MagicMock

class TestDBPedia(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # This test steps through the "search" code
    def testSearch_empty(self):
        real_search_object = DBPedia.DBPediaAPI()
        mock_return = {'results': []}
        mock_return_json = json.dumps(mock_return)
        requests.get = Mock(return_value=FakeResponse(text=mock_return_json))
        query_result = real_search_object.search("blahblahblah")
        self.assertFalse(query_result.has_results())
        self.assertTrue(query_result.get_responses().__len__() == 0)
        self.assertEqual(query_result.__str__(), "Error: No Result")
        self.assertEqual(query_result.__repr__(), query_result.__str__())

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

class FakeResponse:
    def __init__(self, text):
        self.text = text
