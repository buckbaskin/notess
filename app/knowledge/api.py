from app import server as router
from app.knowledge.watson import watson
from app.knowledge.dbpedia import depedia


import json

from flask import make_response, request

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
        if (float(keywords_parsed[i]['relevance']) > threshold):
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
    for i in range(0, num_keywords):
        print(keywords[i]['relevance'])
        sum_relevance = float(keywords[i]['relevance']) + sum_relevance
    threshold = sum_relevance / num_keywords
    return threshold

@router.route('/get_descriptions', methods=['GET'])
def get_descriptions():
    # requires that the request content type be set to application/json
    try:
        keywords = request.args['keywords']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_TEXT)
    dict = {}
    for keyword in keywords:
        dict[keyword] = depedia.DBPediaAPI.search(keyword).get_first_description()
    return json.dumps(dict)

