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
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_TEXT)
    return watson_api(text)