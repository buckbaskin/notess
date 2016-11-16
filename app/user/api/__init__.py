from app import server as router

import json
import bson.json_util as mongo_json

from flask import make_response, request

from app.store.database import Database

INVALID_REQUEST_NO_USER = ('Invalid Request. user_id not found in request.', 400,)
INVALID_REQUEST_NO_CLASS = ('Invalid Request. class_id not found in request.', 400,)
INVALID_REQUEST_NO_NOTE = ('Invalid Request. note_id not found in request.', 400,)
INVALID_REQUEST_NO_TRANSCRIPT = ('Invalid Request. transcript_id not found in request.', 400,)
USER_NOT_FOUND = ('User not found', 404)
NOTE_SAVED = ('Note Saved.', 200)
CLASS_SAVED = ('Class Saved.', 200)

db = Database()

@router.route('/v1/users/create', methods=['POST'])
def create_one_user():
    '''
    Required: indicate the user as a url parameter, but the password must be
    in a valid json dict in the POST body.
    body = '{"password": "insert password here"}'
    '''
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        json_dict = request.get_json()
        password = json_dict['password']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    proposed_response = db.add_user(username)
    return mongo_json.dumps(proposed_response)


@router.route('/v1/users/one', methods=['GET', 'POST'])
def get_one_user():
    # requires that the request content type be set to application/json
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    user_from_database = db.get_user(username)
 
    if not isinstance(user_from_database, dict):
        return make_response(*USER_NOT_FOUND)

    try:
        del user_from_database['password']
    except KeyError:
        # no password information in the dict
        pass

    return mongo_json.dumps(user_from_database)

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

@router.route('/v1/class/new', methods=['POST'])
def create_new_class():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_id = request.args['class_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    class_metadata = {'class_id': 'abcd'}
    if 'class_name' in request.args:
        class_metadata['class_name'] = request.args['class_name']
    return json.dumps(class_metadata)

@router.route('/v1/class/save', methods=['POST'])
def save_existing_class():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_id = request.args['class_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    content = request.get_json()
    return make_response(*CLASS_SAVED)

@router.route('/v1/note/all', methods=['GET'])
def get_all_notes():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    notes_from_database = [{'note_id': 'a1234',
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
    notes_from_database = [{'note_id': 'a1234',
                            'class_id': class_id,
                            'user_id': user_id,
                            'note_name': 'This is the best lecture ever!',
                            'date_created': '10/16/2016',
                            'date_updated': '10/16/2016'}]
    return json.dumps(notes_from_database)

@router.route('/v1/note/new', methods=['GET'])
def create_new_note():
    '''
    This should be creating updating an existing note
    '''
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    note_metadata = {'note_id': 'a1234',
                     'note_name': 'Untitled',
                     'date_created': 'today',
                     'date_updated': 'today'}
    return json.dumps(note_metadata)

@router.route('/v1/note/save', methods=['POST'])
def save_existing_note():
    '''
    This should be creating updating an existing note
    '''
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_NOTE)

    content = request.get_json()
    return make_response(*NOTE_SAVED)

@router.route('/v1/transcript/all')
def get_all_transcripts():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    transcripts_from_database = [{'transcript_id': 'abcd',
                                  'user_id': user_id,
                                  'note_id': 'a1234',
                                  'text': 'This is the first transcript',
                                  'recording_link': '/recording/usertranscript.mp3',
                                  }]
    return json.dumps(transcripts_from_database)

@router.route('/v1/transcript/class')
def get_class_transcripts():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_id = request.args['class_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    transcripts_from_database = [{'transcript_id': 'abcd',
                                  'user_id': user_id,
                                  'class_id': class_id,
                                  'note_id': 'a1234',
                                  'text': 'This is the first transcript',
                                  'recording_link': '/recording/usertranscript.mp3',
                                  }]
    return json.dumps(transcripts_from_database)

@router.route('/v1/transcript/note')
def get_note_transcripts():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_NOTE)
    transcripts_from_database = [{'transcript_id': 'abcd',
                                  'user_id': user_id,
                                  'note_id': note_id,
                                  'text': 'This is the first transcript',
                                  'recording_link': '/recording/usertranscript.mp3',
                                  }]
    return json.dumps(transcripts_from_database)

@router.route('/v1/keyword/all')
def get_all_keywords():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    keywords_from_database = [{'keyword_id': 'qwert',
                               'transcript_id': 'abcd',
                               'user_id': user_id,
                               'keyword': 'Waterfall Model',
                               'short_description': 'A developer horror story',
                               'long_description': 'This is a development process that requires excessive documentation',
                               'link_dbpedia': 'insert dbpedia link here',
                               'link_wikipedia': 'insert wikipedia link here'}]
    return json.dumps(keywords_from_database)

@router.route('/v1/keyword/class')
def get_class_keywords():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_id = request.args['class_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    keywords_from_database = [{'keyword_id': 'qwert',
                               'transcript_id': 'abcd',
                               'user_id': user_id,
                               'class_id': class_id,
                               'keyword': 'Waterfall Model',
                               'short_description': 'A developer horror story',
                               'long_description': 'This is a development process that requires excessive documentation',
                               'link_dbpedia': 'insert dbpedia link here',
                               'link_wikipedia': 'insert wikipedia link here'}]
    return json.dumps(keywords_from_database)

@router.route('/v1/keyword/note')
def get_note_keywords():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_NOTE)
    keywords_from_database = [{'keyword_id': 'qwert',
                               'transcript_id': 'abcd',
                               'user_id': user_id,
                               'note_id': note_id,
                               'keyword': 'Waterfall Model',
                               'short_description': 'A developer horror story',
                               'long_description': 'This is a development process that requires excessive documentation',
                               'link_dbpedia': 'insert dbpedia link here',
                               'link_wikipedia': 'insert wikipedia link here'}]
    if 'class_id' in request.args:
        for i in range(0, len(keywords_from_database)):
            keywords_from_database[0]['class_id'] = request.args['class_id']
    return json.dumps(keywords_from_database)

@router.route('/v1/keyword/transcript')
def get_transcript_keywords():
    try:
        user_id = request.args['user_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        transcript_id = request.args['transcript_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_TRANSCRIPT)
    keywords_from_database = [{'keyword_id': 'qwert',
                               'transcript_id': transcript_id,
                               'user_id': user_id,
                               'keyword': 'Waterfall Model',
                               'short_description': 'A developer horror story',
                               'long_description': 'This is a development process that requires excessive documentation',
                               'link_dbpedia': 'insert dbpedia link here',
                               'link_wikipedia': 'insert wikipedia link here'}]

    if 'class_id' in request.args:
        for i in range(0, len(keywords_from_database)):
            keywords_from_database[0]['class_id'] = request.args['class_id']
    if 'note_id' in request.args:
        for i in range(0, len(keywords_from_database)):
            keywords_from_database[0]['note_id'] = request.args['note_id']
    return json.dumps(keywords_from_database)

