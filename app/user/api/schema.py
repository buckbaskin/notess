from jsonschema import validate

str = {'type': 'string'}
id = {'type': 'object',
      'properties': {
          '$oid': str
      },
      'required': ['$oid']
}

user_schema = {
    'type': 'object',
    'properties': {
        'username': str,
        'email': str,
        'first_name': str,
        'last_name': str,
        'created': {},
        'updated': {}
    },
    'required': ['username', 'email', 'first_name', 'last_name']
}
user_list = {'type': 'array',
             'items': user_schema}

class_schema = {
    'type': 'object',
    'properties': {
        'class_name': str,
        'created': str,
        'modified': str,
        'username': str,
        'metadata': {}
    },
    'required': ['class_name', 'username']
}
class_list = {'type': 'array',
             'items': class_schema}

note_schema = {
    'type': 'object',
    'properties': {
        '_id': id,
        'note_name': str,
        'date_created': str,
        'date_modified': str,
        'class_name': str,
        'username': str
    },
    'required': ['_id', 'note_name', 'class_name']
}
note_list = {'type': 'array',
             'items': note_schema}

transcript_schema = {
    'type': 'object',
    'properties': {
        '_id': id,
        'note_id': id,
        'class_name': str,
        'username': str,
        'text': str,
        'recording_link': str
    },
    'required': ['_id', 'note_id', 'text', 'recording_link']
}
transcript_list = {'type': 'array',
             'items': transcript_schema}

keyword_schema = {
    'type': 'object',
    'properties': {
        '_id': id,
        'transcript_id': id,
        'class_name': str,
        'note_id': id,
        'username': str,
        'text': str,
        'short_description': str,
        'long_description': str,
        'link_dbpedia': str,
        'link_wikipedia': str
    },
    'required': ['_id', 'transcript_id', 'text', 'link_dbpedia', 'link_wikipedia']
}
keyword_list = {'type': 'array',
                'items': keyword_schema}
