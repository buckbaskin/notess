import requests
import json


class DBPediaAPI:

    def search(self, keyword):  # => json_response
        uri_string = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + keyword
        headers = {'Accept': 'application/json'}
        response = requests.get(url=uri_string, headers=headers)
        result = DBPediaAPI.QueryResult(keyword=keyword, json_string=response.text)
        return result

    class QueryResult:
        json_dict = ''
        keyword = ''

        def __init__(self, keyword, json_string):
            self.keyword = keyword
            self.json_dict = json.loads(json_string)

        def has_results(self):
            return len(self.json_dict['results']) > 0

        def __bool__(self):
            return self.has_results()

        def get_first_description(self):
            ''' Get the default description associated with the keyword
            :return: a string of description associated with the keyword included.
            '''
            return self.json_dict['results'][0]['description']

        def get_responses(self):
            ''' Get all DBPedia responses associated with the keyword
            :return: a list of dictionaries associated with each response for the keyword included.
            '''
            return self.json_dict['results']

        def get_descriptions(self):
            ''' Get descriptions associated with the keyword
            :return: a list of descriptions associated with the keyword included.
            '''
            responses = self.json_dict['results']
            descriptions = []
            for response in responses:
                descriptions.append(response['description'])
            return descriptions

        def __str__(self):
            if self:
                return self.get_first_description()
            else:
                return "Error: No Result"

        def __repr__(self):
            return self.__str__()
