from app import server as router
from app.knowledge.dbpedia import depedia

import json
import multiprocessing

from flask import make_response, request

INVALID_REQUEST_NO_KEYWORDS = ('Invalid Request. Keywords not found in request.', 400,)


@router.route('/get_descriptions', methods=['GET'])
def get_descriptions():
    # requires that the request content type be set to application/json
    # request should be {'keywords': [{'text': 'w1', 'relevance': '0.946172'}, {'text': 'w2', 'relevance': '0.78827'}]}
    try:
        keywords_dict = request.args['keywords']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_KEYWORDS)
    return add_descriptions_to_keywords_dict(keywords_dict)


def add_descriptions_to_keywords_dict(keyword_dict_list):
    with multiprocessing.Pool(10) as p:
        p.map(add_description, keyword_dict_list)
    return json.dumps(keyword_dict_list)


def add_description(keyword_dict):
    lookup_result = depedia.DBPediaAPI.search(keyword_dict['text'])
    if lookup_result.has_results():
        keyword_dict['description'] = lookup_result.get_first_description()
    else:
        keyword_dict['description'] = ""

if __name__ == "__main__":
    mock_keyword_list = [{'text': 'sequential design process', 'relevance': '0.946172'},
                         {'text': 'software development processes', 'relevance': '0.78827'},
                         {'text': 'waterfall model', 'relevance': '0.645009'},
                         {'text': 'downwards', 'relevance': '0.347695'},
                         {'text': 'Initiation', 'relevance': '0.282907'}]
    mock_keyword_request_arg = {'keywords': mock_keyword_list}
    mock_incoming_request = json.dumps(mock_keyword_request_arg)
    print(mock_incoming_request)
    parsed_request = json.loads(mock_incoming_request)
    parsed_keywords_list = parsed_request['keywords']
    print(add_descriptions_to_keywords_dict(parsed_keywords_list))
