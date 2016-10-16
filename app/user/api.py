from app import server as router

import json

from flask import make_response, request

INVALID_REQUEST_NO_USER = ('Invalid Request. \'user_id\' not found in request.', 400,)
INVALID_REQUEST_NO_CLASS = ('Invalid Request. \'class_id\' not found in request.', 400,)

@router.route('/v1/users/one', methods=['GET'])
def get_one_user():
    # requires that the request content type be set to application/json
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
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

    return json.dumps(user_from_database)

@router.route('/v1/class/all', methods=['GET'])
def get_all_classes():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    classes_from_database = [{'class_id': 'abcdjasdf',
                             'user_id': user_id,
                             'class_name': 'EECS393 - Software Engineering',
                             'date_created': '10/16/2016',
                             'date_updated': '10/16/2016'}]
    return json.dumps(classes_from_database)

@router.route('/v1/note/all', methods=['GET'])
def get_all_notes():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    notes_from_database = [{'node_id': '1234',
                            'class_id': 'abcdjasdf',
                            'user_id': user_id,
                            'note_name': 'This is the best lecture ever!',
                            'date_created': '10/16/2016',
                            'date_updated': '10/16/2016'}]
    return json.dumps(notes_from_database)

@router.route('/v1/note/class', methods=['GET'])
def get_class_notes():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_id = request.args['class_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    notes_from_database = [{'note_id': '1234',
                            'class_id': class_id,
                            'user_id': user_id,
                            'note_name': 'This is the best lecture ever!',
                            'date_created': '10/16/2016',
                            'date_updated': '10/16/2016'}]
    return json.dumps(notes_from_database)

@router.route('/v1/transcript/all')
def get_all_transcripts():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    transcripts_from_database = [{'transcript_id': 'abcd',
                                  'user_id': user_id,
                                  'note_id': '1234',
                                  'text': 'This is the first transcription',
                                  'recording_link': '/recording/usertranscript.mp3',
                                  }]
