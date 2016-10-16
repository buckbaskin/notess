from app import server as router
from app.knowledge.dbpedia import depedia

import json

from flask import make_response, request

INVALID_REQUEST_NO_TEXT = ('Invalid Request. Keywords not found in request.', 400,)


@router.route('/get_descriptions', methods=['GET'])
def get_descriptions():
    # requires that the request content type be set to application/json
    try:
        keywords = request.args['keywords']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_TEXT)
    return get_descriptions_from_keywords(keywords)


def get_descriptions_from_keywords(keywords):
    response_dict = {}
    for keyword in keywords:
        response_dict[keyword] = depedia.DBPediaAPI.search(keyword).get_first_description()
    return json.dumps(response_dict)
