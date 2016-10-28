from app import server

import app.knowledge.api as knowledge
import json
import unittest

ERROR_MESSAGE_DESCRIPTION_ABSENT = "Processed Keyword does not contain proper description key"


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = server.test_client()
        self.add_descriptions_url = '/add_descriptions'

    def tearDown(self):
        pass

    def test_add_descriptions(self):
        mock_keyword_dict_list = [{'text': 'testdatanonsense', 'relevance': '0.99955'}]
        mock_keyword_request_arg = {'keywords': mock_keyword_dict_list}
        mock_incoming_request_data = json.dumps(mock_keyword_request_arg).encode("utf-8")

        response = self.client.post(self.add_descriptions_url, data=mock_incoming_request_data)

        self.assertEqual(response.status_code, 200)

    def test_add_descriptions_to_keywords_dict_no_description(self):
        mock_keyword_dict_list = [{'text': 'blahblahnonsense', 'relevance': '0.90001'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)
        self.assertTrue('description' in processed_keyword_dict_list[0], ERROR_MESSAGE_DESCRIPTION_ABSENT)
        self.assertEqual(processed_keyword_dict_list[0]['description'], "none")

    def test_add_descriptions_to_keywords_dict_extra_element(self):
        mock_keyword_dict_list = [{'text': 'bigtable', 'relevance': '0.90001', 'extras': 'credit'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        self.assertTrue('description' in processed_keyword_dict_list[0], ERROR_MESSAGE_DESCRIPTION_ABSENT)
        self.assertNotEqual(processed_keyword_dict_list[0]['description'], "none")

    def test_add_descriptions_to_keywords_dict_has_description(self):
        mock_keyword_dict_list = [{'text': 'waterfall', 'relevance': '0.93'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        self.assertTrue('description' in processed_keyword_dict_list[0], ERROR_MESSAGE_DESCRIPTION_ABSENT)
        self.assertNotEqual(processed_keyword_dict_list[0]['description'], "none")

    def test_add_descriptions_to_keywords_dict_combined(self):
        mock_keyword_dict_list = [{'text': 'blahblahnonsense', 'relevance': '0.90001'},
                                  {'text': 'bigtable', 'relevance': '0.90002'},
                                  {'text': 'waterfall', 'relevance': '0.93'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        for processed_keyword_dict in processed_keyword_dict_list:
            self.assertTrue('description' in processed_keyword_dict, ERROR_MESSAGE_DESCRIPTION_ABSENT)
