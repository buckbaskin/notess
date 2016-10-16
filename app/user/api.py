from app import server as router

import json

from flask import make_response

INVALID_REQUEST_NO_USER = ('Invalid Request. \'user_id\' not found in request.', 400,)
INVALID_REQUEST_NO_CLASS = ('Invalid Request. \'class_id\' not found in request.', 400,)

@router.route('/v1/users/one', methods=['POST'])
def get_one_user():
    # requires that the request content type be set to application/json
    content = request.get_json()
    try:
        user_id = content['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
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

@router.route('/v1/class/all')
def get_all_classes():
    content = request.get_json()
    try:
        user_id = content['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    classes_from_database = [{'class_id': 'abcdjasdf',
                             'user_id': user_id,
                             'class_name': 'EECS393 - Software Engineering',
                             'date_created': '10/16/2016',
                             'date_updated': '10/16/2016'}]
    return json.dumps(classes_from_database)

@router.route('/v1/note/all')
def get_all_notes():
    content = request.get_json()
    try:
        user_id = content['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    notes_from_database = [{'node_id': '1234',
                            'class_id': 'abcdjasdf',
                            'user_id': user_id,
                            'note_name': 'This is the best lecture ever!',
                            'date_created': '10/16/2016',
                            'date_updated': '10/16/2016'}]
    return json.dumps(notes_from_database)

@router.route('/v1/note/class')
def get_class_notes():
    content = request.get_json()
    try:
        user_id = content['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_id = content['class_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    notes_from_database = [{'node_id': '1234',
                            'class_id': class_id,
                            'user_id': user_id,
                            'note_name': 'This is the best lecture ever!',
                            'date_created': '10/16/2016',
                            'date_updated': '10/16/2016'}]
    return json.dumps(notes_from_database)

