import unittest
import app.knowledge.api as knowledge


class TestAPI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_descriptions_to_keywords_dict_no_description(self):
        error_message_not_added = "Processed Keyword does not contain proper description key"
        mock_keyword_dict_list = [{'text': 'blahblahnonsense', 'relevance': '0.90001'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)
        self.assertTrue('description' in processed_keyword_dict_list[0], error_message_not_added)
        self.assertEqual(processed_keyword_dict_list[0]['description'], "none")

    def test_add_descriptions_to_keywords_dict_extra_element(self):
        error_message_not_added = "Processed Keyword does not contain proper description key"
        mock_keyword_dict_list = [{'text': 'bigtable', 'relevance': '0.90001', 'extras': 'credit'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        self.assertTrue('description' in processed_keyword_dict_list[0], error_message_not_added)
        self.assertNotEqual(processed_keyword_dict_list[0]['description'], "none")

    def test_add_descriptions_to_keywords_dict_has_description(self):
        error_message_not_added = "Processed Keyword does not contain proper description key"
        mock_keyword_dict_list = [{'text': 'waterfall', 'relevance': '0.93'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        self.assertTrue('description' in processed_keyword_dict_list[0], error_message_not_added)
        self.assertNotEqual(processed_keyword_dict_list[0]['description'], "none")

    def test_add_descriptions_to_keywords_dict_combined(self):
        error_message_not_added = "Processed Keyword does not contain proper description key"
        mock_keyword_dict_list = [{'text': 'blahblahnonsense', 'relevance': '0.90001'},
                             {'text': 'bigtable', 'relevance': '0.90002'},
                             {'text': 'waterfall', 'relevance': '0.93'}]

        processed_keyword_dict_list = knowledge.add_descriptions_to_keywords_dict(mock_keyword_dict_list)

        for processed_keyword_dict in processed_keyword_dict_list:
            self.assertTrue('description' in processed_keyword_dict, error_message_not_added)
