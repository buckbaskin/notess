from jsonschema import validate

str = {'type': 'string'}

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
        'note_id': str,
        'note_name': str,
        'date_created': str,
        'date_modified': str,
        'class_id': str,
        'user_id': str
    },
    'required': ['note_id', 'note_name', 'class_id']
}
note_list = {'type': 'array',
             'items': note_schema}

transcript_schema = {
    'type': 'object',
    'properties': {
        'transcript_id': str,
        'note_id': str,
        'class_id': str,
        'user_id': str,
        'text': str,
        'recording_link': str
    },
    'required': ['transcript_id', 'note_id', 'text', 'recording_link']
}
transcript_list = {'type': 'array',
             'items': transcript_schema}

keyword_schema = {
    'type': 'object',
    'properties': {
        'keyword_id': str,
        'transcript_id': str,
        'class_id': str,
        'note_id': str,
        'user_id': str,
        'keyword': str,
        'short_description': str,
        'long_description': str,
        'link_dbpedia': str,
        'link_wikipedia': str
    },
    'required': ['keyword_id', 'transcript_id', 'keyword', 'link_dbpedia', 'link_wikipedia']
}
keyword_list = {'type': 'array',
                'items': keyword_schema}
