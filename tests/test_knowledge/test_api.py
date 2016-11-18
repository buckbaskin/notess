from app import server

import app.knowledge.api as knowledge
import app.knowledge.dbpedia.dbpedia as dbpedia
from unittest.mock import Mock, patch
import json
import unittest

ERROR_MESSAGE_DESCRIPTION_ABSENT = "Processed Keyword does not contain proper description key"


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.add_descriptions_url = '/add_descriptions'

    def tearDown(self):
        pass

    @patch('app.knowledge.dbpedia.dbpedia.DBPediaAPI.search')
    def test_add_descriptions(self, mock_api_search):
        mock_keyword_dict_list = [{'text': 'testdatanonsense', 'relevance': '0.99955'}]

        mock_keyword = "testdatanonsense"
        mock_return = {'results': []}
        mock_return_json = json.dumps(mock_return)
        mock_result = dbpedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mock_api_search.return_value = mock_result
        mock_keyword_request_arg = {'keywords': mock_keyword_dict_list}
        mock_incoming_request_data = json.dumps(mock_keyword_request_arg).encode("utf-8")

        response = self.client.post(self.add_descriptions_url, data=mock_incoming_request_data)

        self.assertEqual(response.status_code, 200)

    @patch('app.knowledge.dbpedia.dbpedia.DBPediaAPI.search')
    def test_add_descriptions_to_keywords_dict_no_description(self, mock_api_search):
        mock_keyword_dict_list = [{'text': 'blahblahnonsense', 'relevance': '0.90001'}]

        mock_keyword = "blahblahnonsense"
        mock_return = {'results': []}
        mock_return_json = json.dumps(mock_return)
        mock_result = dbpedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mock_api_search.return_value = mock_result

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)
        self.assertTrue('description' in processed_keyword_dict_list[0], ERROR_MESSAGE_DESCRIPTION_ABSENT)
        self.assertEqual(processed_keyword_dict_list[0]['description'], "none")

    @patch('app.knowledge.dbpedia.dbpedia.DBPediaAPI.search')
    def test_add_descriptions_to_keywords_dict_extra_element(self, mock_api_search):
        mock_keyword_dict_list = [{'text': 'bigtable', 'relevance': '0.90001', 'extras': 'credit'}]

        mock_keyword = "bigtable"
        mock_return = {'results': [{'description': 'mock_answer1'}]}
        mock_return_json = json.dumps(mock_return)
        mock_result = dbpedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mock_api_search.return_value = mock_result

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        self.assertTrue('description' in processed_keyword_dict_list[0], ERROR_MESSAGE_DESCRIPTION_ABSENT)
        self.assertNotEqual(processed_keyword_dict_list[0]['description'], "none")

    @patch('app.knowledge.dbpedia.dbpedia.DBPediaAPI.search')
    def test_add_descriptions_to_keywords_dict_has_description(self, mock_api_search):
        mock_keyword_dict_list = [{'text': 'waterfall', 'relevance': '0.93'}]

        mock_keyword = "bigtable"
        mock_return = {'results': [{'description': 'mock_answerA'}, {'description': 'mock_answer2'}]}
        mock_return_json = json.dumps(mock_return)
        mock_result = dbpedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mock_api_search.return_value = mock_result

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        self.assertTrue('description' in processed_keyword_dict_list[0], ERROR_MESSAGE_DESCRIPTION_ABSENT)
        self.assertNotEqual(processed_keyword_dict_list[0]['description'], "none")

    @patch('app.knowledge.dbpedia.dbpedia.DBPediaAPI.search')
    def test_add_descriptions_to_keywords_dict_combined(self, mock_api_search):
        mock_keyword_dict_list = [{'text': 'blahblahnonsense', 'relevance': '0.90001'},
                                  {'text': 'bigtable', 'relevance': '0.90002'},
                                  {'text': 'waterfall', 'relevance': '0.93'}]
        mock_keyword = "any"
        mock_return = {'results': []}
        mock_return_json = json.dumps(mock_return)
        mock_result = dbpedia.DBPediaAPI.QueryResult(mock_keyword, mock_return_json)
        mock_api_search.return_value = mock_result
        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        for processed_keyword_dict in processed_keyword_dict_list:
            self.assertTrue('description' in processed_keyword_dict, ERROR_MESSAGE_DESCRIPTION_ABSENT)
