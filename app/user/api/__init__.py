from app import server as router

import json
import bson.json_util as mongo_json
from bson.objectid import ObjectId

from flask import make_response, request

from app.store.database import Database

INVALID_REQUEST_NO_USER = ('Invalid Request. username not found in request.', 400,)
INVALID_REQUEST_NO_CLASS = ('Invalid Request. class_name not found in request.', 400,)
INVALID_REQUEST_NO_NOTE = ('Invalid Request. note_id not found in request.', 400,)
INVALID_REQUEST_NO_TRANSCRIPT = ('Invalid Request. transcript_id not found in request.', 400,)
USER_NOT_FOUND = ('User not found', 404)
CLASS_NOT_FOUND = ('Class not found', 404)
NOTE_NOT_FOUND = ('Note not found', 404)
NOTE_SAVED = ('Note Saved.', 200)
CLASS_SAVED = ('Class Saved.', 200)

db = Database()

def fix_oid(potential_oid):
    if isinstance(potential_oid, str):
        return potential_oid
    if isinstance(potential_oid, dict):
        return potential_oid['$oid']
    return str(potential_oid)

### User API ###

@router.route('/v1/users/new', methods=['POST'])
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
        if not json_dict:
            raise KeyError()
        password = json_dict['password']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    content = request.get_json()
    if not content:
        content = {}
    save_this = {}
    for key in ['email', 'first_name', 'last_name']:
        if key in content:
            save_this[key] = content[key]
        else:
            return make_response('Could not create user. Missing key %s' % (key,))
    proposed_response = db.add_user(username, **save_this)
    return mongo_json.dumps(proposed_response)

@router.route('/v1/users/one', methods=['GET'])
def get_one_user():
    # requires that the request content type be set to application/json
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    user_from_database = db.get_user(username)
 
    if not isinstance(user_from_database, dict):
        print('user %s from_database: %s' % (username, user_from_database,))
        return make_response(*USER_NOT_FOUND)

    try:
        del user_from_database['password']
    except KeyError:
        # no password information in the dict
        pass

    return mongo_json.dumps(user_from_database)

### Class API ###

@router.route('/v1/class/one', methods=['GET'])
def get_one_class():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_name = request.args['class_name']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    classes_from_database = db.get_class(username, class_name)
    return mongo_json.dumps(classes_from_database)

@router.route('/v1/class/all', methods=['GET'])
def get_all_classes():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    print('debug: GET all classes for username: %s' % (username,))
    classes_from_database = db.get_all_classes(username)
    return mongo_json.dumps(classes_from_database)

@router.route('/v1/class/new', methods=['POST'])
def create_new_class():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_name = request.args['class_name']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    class_metadata = request.get_json()
    if not class_metadata:
        class_metadata = {}
    if 'class_name' in request.args:
        class_metadata['class_name'] = request.args['class_name']

    created_class = db.add_class(username, class_name)
    result = mongo_json.dumps(created_class)
    return result

@router.route('/v1/class/update', methods=['POST'])
def save_existing_class():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_name = request.args['class_name']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    content = request.get_json()
    if not content:
        return make_response('Could note update class. No content provided', 400)
    print('update with new content %s' % (content,))
    updated_class = db.update_class(username, class_name, content)
    return mongo_json.dumps(updated_class)

### Note API ###

@router.route('/v1/note/all', methods=['GET'])
def get_all_notes():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    print('debug: GET all notes for username: %s' % (username,))
    results = db.get_all_notes(username)
    if results is None:
        return make_response(*INVALID_REQUEST_NO_NOTE)
    return mongo_json.dumps(results)

@router.route('/v1/note/class', methods=['GET'])
def get_class_notes():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_name = request.args['class_name']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    print('debug: GET all notes for  username %s for class %s' % (username, class_name,))
    notes_from_database = db.get_all_notes(username, class_name)
    return mongo_json.dumps(notes_from_database)

@router.route('/v1/note/new', methods=['POST'])
def create_new_note():
    '''
    This should be creating a new note
    '''
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    content = request.get_json()
    if not content:
        return make_response('Could not create new note. No JSON note information was POSTed', 400)
    save_this = {}
    for key in ['class_name', 'note_name', 'text']:
        if key in content:
            save_this[key] = content[key]
        else:
            make_response('New note could not be created, missing field %s' % (key,), 400)
    print('debug: %s' % (content,))
    print('debug: POST create note for username: %s' % (username,))
    print('debug:      { class_name: %s' % (save_this['class_name'],))
    print('debug:        note_name: %s }' % (save_this['note_name'],))
    return mongo_json.dumps(db.add_note(username, save_this['class_name'], save_this['note_name'], save_this['text']))

@router.route('/v1/note/update', methods=['POST'])
def save_existing_note():
    '''
    This should be updating an existing note
    '''
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_NOTE)

    content = request.get_json()
    if not content:
        return make_response('Could not update note. No JSON note information was POSTed', 400)

    save_this = {}

    print('content as loaded: %s' % (content,))
    print('content keys: %s' % (content.keys()))
    for key in content:
        if len(key) >= 2 and key[-2:] == 'id':
            print('fix this: %s' % (key,))
            save_this[key] = fix_oid(content[key])
        else:
            print('keep this the same %s' % (key,))
            save_this[key] = content[key]

    update_result = db.update_note(username, note_id, save_this)
    if update_result is None:
        return make_response('Note_id not found in database for this user', 404)
    # if not isinstance(update_result, dict):
    print('debug: POST update note %s for username: %s' % (username, note_id,))
    print('debug:      {')
    for key in save_this:
        value = save_this[key]
        value_str = str(value)
        if len(value_str) > 80:
            value_str = value_str[:76] + ' ...'
        print('debug:        %s : %s' % (key, value_str,))
    print('debug:      }')

    return mongo_json.dumps(update_result)

@router.route('/v1/transcript/new', methods=['POST'])
def create_transcript():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_NOTE)
    content = request.get_json()
    if not content:
        content = {}
    save_this = {}
    for key in ['text', 'recording_link']:
        if key in content and key[-3:] == '_id':
            save_this[key] = fix_oid(content[key])
        elif key in content:
            save_this[key] = content[key]
        else:
            return make_response('Could not create transcript. Key %s not found in POST' % (key,), 400)

    print('debug: POST create new transcript for username %s note %s' % (username, note_id,))
    print('debug:      {')
    if len(save_this['text']) < 80:
        print('debug:        %s : %s' % ('text', save_this['text']))
    else:
        print('debug:        %s : %s' % ('text', save_this['text'][:76]+' ...'))
    print('debug:        %s : %s' % ('recording_link', save_this['recording_link']))
    print('debug:      }')
    
    return mongo_json.dumps(db.add_transcript(username, note_id, **save_this))

@router.route('/v1/transcript/all', methods=['GET'])
def get_all_transcripts():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    transcripts_from_database = db.get_all_transcripts(username)
    return mongo_json.dumps(transcripts_from_database)

@router.route('/v1/transcript/note', methods=['GET'])
def get_note_transcripts():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_NOTE)
    print('debug: GET transcripts for username %s note %s' % (username, note_id,))
    transcripts_from_database = db.get_all_transcripts(username, note_id=note_id)
    return mongo_json.dumps(transcripts_from_database)

@router.route('/v1/keyword/new', methods=['POST'])
def add_keyword():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    # username: str, note_id: str, transcript_id: str, text: str, relevance: float, description: str
    content = request.get_json()
    if not content:
        content = {}
    save_this = {}
    for key in ['note_id', 'transcript_id', 'text', 'relevance', 'description', 'link_dbpedia', 'link_wikipedia']:
        if key in content and key[-3:] == '_id':
            save_this[key] = fix_oid(content[key])
        elif key in content:
            save_this[key] = content[key]
        else:
            return make_response('Could not create keyword, missing field %s in POSTed JSON' % key, 400)

    return mongo_json.dumps(db.add_keyword(username, **save_this))

@router.route('/v1/keyword/all', methods=['GET'])
def get_all_keywords():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    keywords_from_database = db.get_all_keywords(username)
    return mongo_json.dumps(keywords_from_database)

@router.route('/v1/keyword/class', methods=['GET'])
def get_class_keywords():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        class_name = request.args['class_name']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_CLASS)
    keywords_from_database = db.get_all_keywords(username, class_name=class_name)
    return mongo_json.dumps(keywords_from_database)

@router.route('/v1/keyword/note', methods=['GET'])
def get_note_keywords():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_NOTE)
    keywords_from_database = db.get_all_keywords(username, note_id=note_id)
    return mongo_json.dumps(keywords_from_database)

@router.route('/v1/keyword/transcript', methods=['GET'])
def get_transcript_keywords():
    try:
        username = request.args['username']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_USER)
    try:
        transcript_id = request.args['transcript_id']
    except KeyError:
        return make_response(*INVALID_REQUEST_NO_TRANSCRIPT)
    keywords_from_database = db.get_all_keywords(username, transcript_id=transcript_id)
    return mongo_json.dumps(keywords_from_database)

