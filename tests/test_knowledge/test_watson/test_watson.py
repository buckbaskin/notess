import unittest
import json
from app.knowledge.api import compute_threshold, prune_keywords

class TestWatson(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testComputeThreshold_sameRelevance(self):
        mock_keyword_list = [{"text": "sequential design process", "relevance": "0.5"},
                             {"text": "software development processes", "relevance": "0.5"},
                             {"text": "waterfall model", "relevance": "0.5"},
                             {"text": "downwards", "relevance": "0.5"},
                             {"text": "Initiation", "relevance": "0.5"}]
        self.assertEqual(0.5, compute_threshold(mock_keyword_list));

    def testComputeThreshold_uniqueRelevance(self):
        mock_keyword_list = [{"text": "sequential design process", "relevance": "0.1"},
                             {"text": "software development processes", "relevance": "0.6"},
                             {"text": "waterfall model", "relevance": "0.9"},
                             {"text": "downwards", "relevance": "0.4"},
                             {"text": "Initiation", "relevance": "0.2"}]
        self.assertEqual(0.44000000000000006, compute_threshold(mock_keyword_list));

    def testComputeThreshold_emptyList(self):
        mock_keyword_list = []
        self.assertEqual(0, compute_threshold(mock_keyword_list));

    def testPruneList_noPruning(self):
        mock_keyword_list = [{"text": "sequential design process", "relevance": "0.5"},
                             {"text": "software development processes", "relevance": "0.5"},
                             {"text": "waterfall model", "relevance": "0.5"},
                             {"text": "downwards", "relevance": "0.5"},
                             {"text": "Initiation", "relevance": "0.5"}]
        mock_incoming_request = json.dumps(mock_keyword_list);
        self.assertEqual(mock_incoming_request, prune_keywords(mock_incoming_request));

    def testPruneList_somePruning(self):
        mock_keyword_list = [{"text": "sequential design process", "relevance": "0.1"},
                             {"text": "software development processes", "relevance": "0.1"},
                             {"text": "waterfall model", "relevance": "0.5"},
                             {"text": "downwards", "relevance": "0.5"},
                             {"text": "Initiation", "relevance": "0.5"}]
        mock_incoming_request = json.dumps(mock_keyword_list);

        mock_keyword_list_returned = [{"text": "waterfall model", "relevance": "0.5"},
                             {"text": "downwards", "relevance": "0.5"},
                             {"text": "Initiation", "relevance": "0.5"}]
        mock_incoming_request_returned = json.dumps(mock_keyword_list_returned);
        self.assertEqual(mock_incoming_request_returned, prune_keywords(mock_incoming_request));

if __name__ == "__main__":
    d = TestWatson()
    d.testComputeThreshold();