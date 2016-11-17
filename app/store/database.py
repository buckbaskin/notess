import pymongo
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
import gridfs

import datetime

class Database(object):
    def __init__(self):
        self._client = MongoClient('localhost', 27017)
        self._db = self._client['user']

        self._user_collection = self._db.user
        self._user_collection.create_index('username', unique=True)

        self._class_collection = self._db['class']
        self._class_collection.create_index([('username', pymongo.ASCENDING,), ('class_name', pymongo.ASCENDING,)], unique=True)

        self._note_collection = self._db.note
        self._note_collection.create_index([('_id', pymongo.ASCENDING), ('username', pymongo.ASCENDING)])
        
        self._transcript_collection = self._db.transcript
        self._transcript_collection.create_index([('_id', pymongo.ASCENDING), ('username', pymongo.ASCENDING)])

        self._keyword_collection = self._db.keyword_forward
        self._keyword_collection.create_index([('_id', pymongo.ASCENDING), ('username', pymongo.ASCENDING)])
        self._keyword_rev_index = self._db.keyword_index
        self._keyword_rev_index.create_index('text', unique=True)

        self._fileclient = gridfs.GridFS(self._client['gridfs'])

    ### User Database ###

    def add_user(self, username, first_name, last_name, email):
        user = {
            'username': username,
            'email': email,
            'created': datetime.datetime.utcnow(),
            'updated': datetime.datetime.utcnow()
        }
        try:
            user_id = self._user_collection.insert_one(user).inserted_id
        except pymongo.errors.DuplicateKeyError:
            pass
        return self.get_user(username)

    def update_user(self, username):
        user = self.get_user(username)
        user['updated'] = datetime.datetime.utcnow()
        self._user_collection.update_one({'username': username}, {'$set', user})
        return self.get_user(username)

    def get_user(self, username):
        user_result = self._user_collection.find_one({'username': username}, {'password': 0, '_id': 0})
        return user_result

    def delete_user(self, username):
        user_result = self._user_collection.delete_one({'username': username})
        class_result = self.delete_all_classes(username)
        notes_result = self.delete_all_notes(username)
        return user_result.deleted_count

    ### Class Database ###

    def add_class(self, username, class_name):
        class_ = {
            'version': 0,
            'username': username,
            'class_name': class_name
        }
        class_id = self._class_collection.insert_one(class_).inserted_id
        return self.get_class(username, class_name)

    def update_class(self, username, class_name, content):
        if 'version' in content:
            del content['version']
        self._class_collection.update_one({'_id': ObjectId(str(class_name))}, {'$set': content, '$inc': {'version': 1}})
        return self.get_class(username, class_name)

    def get_class(self, username, class_name):
        class_result = self._class_collection.find_one({'username': username, '_id': ObjectId(str(class_name))})
        return class_result

    def get_all_classes(self, username):
        class_result = self._class_collection.find({'username': username})
        return class_result

    def delete_class(self, username, class_name):
        result = self._class_collection.delete_one({'username': username, 'class_name': class_name})
        return result.deleted_count

    def delete_all_classes(self, username):
        result = self._class_collection.delete_many({'username': username})
        return result.deleted_count

    ### Notes Database ###

    def add_note(self, username: str, class_name: str, note_name: str):
        note = {
            'username': username,
            'class_name': class_name,
            'note_name': note_name
        }
        note_id = self._note_collection.insert_one(note).inserted_id
        return self.get_note(username, note_id)

    def update_note(self, username, note_id, content):
        self._note_collection.update_one({'username': username, '_id': ObjectId(str(note_id))}, {'$set': content})
        return self.get_note(username, note_id)

    def get_note(self, username, note_id):
        # require username because it might return different stuff for a note shared between users
        result = self._note_collection.find_one({'_id': ObjectId(note_id)})
        return result

    def get_all_notes(self, username, class_name=None):
        if class_name is None:
            result = self._note_collection.find({'username': username})
        else:
            result = self._note_collection.find({'username': username, 'class_name': class_name})
        return result

    def delete_note(self, username, note_id) -> int:
        result = self._note_collection.delete_one({'_id': ObjectId(note_id), 'username': username})
        return result.deleted_count

    def delete_all_notes(self, username) -> int:
        result = self._note_collection.delete_many({'username': username})
        return result.deleted_count

    ### Transcript Database ###

    def add_transcript(self, username: str, note_id: str, text: str):
        transcript = {
            'username': username,
            'note_id': ObjectId(note_id),
            'text': text
        }
        transcript_id = self._transcript_collection.insert_one(transcript).inserted_id
        return self.get_transcript(username, transcript_id)

    def update_transcript(self, username, transcript_id):
        # TODO
        return self.get_transcript(username, transcript_id)

    def get_transcript(self, username, transcript_id):
        # require username because it might return different stuff for a transcript shared between users
        result = self._transcript_collection.find_one({'_id': ObjectId(transcript_id)})
        return result

    def get_all_transcripts(self, username, note_id=None):
        if note_id is None:
            result = self._transcript_collection.find({'username': username})
        else:
            result = self._transcript_collection.find({'username': username, 'node_id': ObjectId(str(note_id))})
        return result

    def delete_transcript(self, username, transcript_id) -> int:
        result = self._transcript_collection.delete_one({'_id': ObjectId(transcript_id), 'username': username})
        return result.deleted_count

    def delete_all_transcripts(self, username) -> int:
        result = self._transcript_collection.delete_many({'username': username})
        return result.deleted_count

    ### Keyword Database ###

    def add_keyword(self, username: str, note_id: str, transcript_id: str, text: str, relevance: float, description: str):
        keyword = {
            'username': username,
            'note_id': note_id,
            'transcript_id': transcript_id,
            'text': text,
            'relevance': relevance,
            'description': description
        }
        keyword_id = self._keyword_collection.insert_one(keyword).inserted_id
        self._keyword_rev_index.find_one_and_update(
            {'text': text},
            {'$addToSet': {'instances': [note_id]}},
            upsert=True,
            return_document =ReturnDocument.AFTER
        )
        return self.get_keyword(username, keyword_id)

    def update_keyword(self, username, keyword_id):
        # TODO
        return self.get_keyword(username, keyword_id)

    def get_keyword(self, username, keyword_id):
        # require username because it might return different stuff for a keyword shared between users
        result = self._keyword_collection.find_one({'_id': ObjectId(keyword_id), 'username': username})
        return result

    def get_all_keywords(self, username, class_name=None, note_id=None, transcript_id=None):
        if class_name is not None:
            result = self._keyword_collection.find({'username': username, 'class_name': class_name})
        if note_id is not None:
            result = self._keyword_collection.find({'username': username, 'note_id': ObjectId(note_id)})
        if transcript_id is not None:
            result = self._keyword_collection.find({'username': username, 'note_id': ObjectId(note_id)})
        else:
            result = self._keyword_collection.find({'username': username})
        return result

    def delete_keyword(self, username, keyword_id) -> int:
        result = self._keyword_collection.delete_one({'_id': ObjectId(keyword_id), 'username': username})
        return result.deleted_count

    def delete_all_keywords(self, username) -> int:
        result = self._keyword_collection.delete_many({'username': username})
        return result.deleted_count

    ### Audio Database ###

    def write_audio(self, file_, filename, content_type='audio/mpeg'):
        file_id = self._fileclient.put(file_, filename=filename, content_type=content_type)
        return file_id

    def read_audio(self, file_id):
        with self._fileclient.get(file_id) as f:
            return f.read()

