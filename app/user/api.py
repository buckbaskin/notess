from app import server as router

import json

from flask import make_response

@router.route('/v1/users/one', methods=['POST'])
def get_one_user():
    # requires that the request content type be set to application/json
    content = request.get_json()
    try:
        user_id = content['user_id']
    except KeyError:
        return make_response('Invalid Request. \'user_id\' not found in request.', 400)
    print(content)
    user_from_database = {'user_id': user_id,
                          'username': 'johndoe',
                          'email': 'johndoe@gmail.com',
                          'first_name': 'John',
                          'last_name': 'Doe'}
    try:
        del user_from_database['password']
    except KeyError:
        # no password information in the dict
        pass

    return json.dumps(user)

