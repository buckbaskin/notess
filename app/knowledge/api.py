from app import server as router
from app.knowledge.watson import watson
from app.knowledge.dbpedia import dbpedia
from flask import make_response, request

import json
from jsonschema import validate
from app.knowledge.dbpedia.schema import dbpedia_schema

INVALID_REQUEST_NO_KEYWORDS = ('Invalid Request. Keywords not found in request.', 400,)
INVALID_REQUEST_NO_TEXT = ('Invalid Request. Text not found in request.', 400,)


@router.route('/get_keywords', methods=['GET'])
def get_keywords():
    """
    Given a string, get keywords
    :return:
    """
    watson_api = watson.WatsonAPI();
    # requires that the request content type be set to application/json
    try:
        text = request.args['text']
        print(text)
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_TEXT)
    keywords = prune_keywords(watson_api.get_keywords(text))
    return keywords


def prune_keywords(keywords):
    """
    Given json object of keywords, prune those that have a relevance below the threshold
    :param keywords: A json object of keywords and relevances
    :return: A json object of keywords and relevance for those that are above the threshold
    """
    keywords_parsed = json.loads(keywords)
    threshold = compute_threshold(keywords_parsed)
    num_keywords = len(keywords_parsed)
    valid_keywords = []
    print(keywords_parsed)
    for i in range(0, num_keywords):
        if (float(keywords_parsed[i]['relevance']) >= threshold):
            valid_keywords.append(keywords_parsed[i])
    print(json.dumps(valid_keywords))
    return json.dumps(valid_keywords)


def compute_threshold(keywords):
    """
    Compute the threshold by averaging all keyword relevances
    :param keywords: Json object of keywords and relevances
    :return: the computed threshold as double
    """
    sum_relevance = 0.0
    num_keywords = len(keywords)
    if (num_keywords == 0):
        return 0;
    for i in range(0, num_keywords):
        print(keywords[i]['relevance'])
        sum_relevance = float(keywords[i]['relevance']) + sum_relevance
    threshold = sum_relevance / num_keywords
    return threshold

@router.route('/add_descriptions', methods=['POST'])
def add_descriptions():
    # requires that the request content type be set to application/json
    # request should be {'keywords': [{'text': 'w1', 'relevance': '0.946172'}, {'text': 'w2', 'relevance': '0.78827'}]}
    decoded_json = request.get_data().decode("utf-8")
    data_object = json.loads(decoded_json)
    validate(data_object, dbpedia_schema)
    keywords_dict_list = data_object['keywords']
    processed_keywords_dict_list = add_descriptions_to_keywords_dict(keywords_dict_list)
    return_data = {'keywords': processed_keywords_dict_list}
    return json.dumps(return_data)


def add_descriptions_to_keywords_dict(keyword_dict_list):
    api_object = dbpedia.DBPediaAPI()
    for keyword_dict in keyword_dict_list:
        description_set = False;
        lookup_result = api_object.search(keyword_dict['text'])
        if lookup_result.has_results():
            keyword_dict['description'] = lookup_result.get_first_description()
            description_set = True
        else:
            keyword_words = keyword_dict['text'].split(" ")
            for word in reversed(keyword_words):
                lookup_result = api_object.search(word)
                if lookup_result.has_results():
                    keyword_dict['description'] = lookup_result.get_first_description()
                    description_set = True;
                    break;
        if not description_set:
            keyword_dict['description'] = "none"
    return keyword_dict_list

