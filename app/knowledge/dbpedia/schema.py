str = {'type': 'string'}

keyword_elements = {
    'type': 'object',
    'properties': {
        'text': str,
        'relevance': {'type': 'number'}
    }
    'required': ['text', 'relevance']
}

keyword_list = {'type': 'array',
                'items': keyword_elements}

dbpedia_schema = {
    'type': 'object',
    'properties': {
        'keywords': keyword_list
    },
    'required': ['keywords']
}
