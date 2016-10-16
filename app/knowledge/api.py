from app import server as router
from app.knowledge.watson import watson

import json

from flask import make_response, request

INVALID_REQUEST_NO_TEXT = ('Invalid Request. Text not found in request.', 400,)

@router.route('/get_keywords', methods=['GET'])
def get_keywords():
    watson_api = watson.WatsonAPI();
    # requires that the request content type be set to application/json
    try:
        text = request.args['text']
        print("*****" + text)
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_TEXT)
    keywords = prune_keywords(watson_api.get_keywords(text))
    return keywords


def prune_keywords(keywords):
    keywords_parsed = json.loads(keywords)
    threshold = compute_threshold(keywords_parsed)
    num_keywords = len(keywords_parsed)
    valid_keywords = []
    print(keywords_parsed)
    for i in range(0, num_keywords):
        if (float(keywords_parsed[i]['relevance']) > threshold):
            valid_keywords.append(keywords_parsed[i])
    print(json.dumps(valid_keywords))
    return valid_keywords

def compute_threshold(keywords):
    sum_relevance = 0.0
    num_keywords = len(keywords)
    for i in range(0, num_keywords):
        print(keywords[i]['relevance'])
        sum_relevance = float(keywords[i]['relevance']) + sum_relevance
    threshold = sum_relevance / num_keywords
    return threshold