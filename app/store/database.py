from pymongo import MongoClient, Connection
import gridfs

import datetime

class Database(object):
    def __init__(self):
        self._client = MongoClient('localhost', 27017)
        self._db = self._client('user')

        self._user_collection = self._db.user
        self._user_collection.create_index('username', unique=True)

        self._class_collection = self._db.class
        self._class_collection.create_index(['username', 'class_name'], unique=True)

        self._connection = Connection()
        self._fileclient = gridfs.GridFS(self._connection.gridfs)

    ### User Database ###

    def add_user(self, username):
        user = {
            'username': username,
            'created': datetime.datetime.utcnow()
            'updated': datetime.datetime.utcnow()
        }
        user_id = self._user_collection.insert_one(user).inserted_id
        return self.get_user(username)

    def update_user(self, username):
        user = self.get_user(username)
        user['updated'] = datetime.datetime.utcnow()
        self._user_collection.update_one({'username': username}, {'$set', user})
        return self.get_user(username)

    def get_user(self, username):
        user_result = self._user_collection.find_one({'username': username})
        return user_result

    def delete_user(self, username):
        user_result = self._user_collection.delete_one({'username': username})
        class_result = self.delete_all_classes(username)
        return user_result.deleted_count

    ### Class Database ###

    def add_class(self, username, class_name):
        # TODO
        return self.get_class(username, class_name)

    def update_class(self, username, class_name):
        # TODO
        return self.get_class(username, class_name)

    def get_class(self, username, class_name):
        class_result = self._class_collection.find_one({'username': username, 'class_name': class_name})
        return class_result

    def delete_class(self, username, class_name):
        result = self._class_collection.delete_one({'username': username, 'class_name': class_name})
        return result.deleted_count

    def delete_all_classes(self, username):
        result = self._class_collection.delete_many({'username': username})
        return result.deleted_count

    ### Audio Database ###

    def write_audio(self, file_, filename, content_type='audio/mpeg'):
        file_id = self._fileclient.put(file_, filename=filename, content_type=content_type)
        return file_id

    def read_audio(self, file_id):
        with fs.get(file_id) as f:
            return f.read()

