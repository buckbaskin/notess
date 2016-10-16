import requests
import json


class DBPediaAPI:

    @staticmethod
    def search(keyword):  # => json_response
        uri_string = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + keyword
        headers = {'Accept': 'application/json'}
        response = requests.get(url=uri_string, headers=headers)
        result = DBPediaAPI.QueryResult(json_string=response.text)
        return result

    class QueryResult:
        json_dict = ''

        def __init__(self, json_string):
            self.json_dict = json.loads(json_string)

        def has_result(self):
            return len(self.json_dict['results']) > 0

        def __bool__(self):
            return self.has_result()

        def get_first_description(self):
            return self.json_dict['results'][0]['description']

        def __str__(self):
            if self:
                return self.get_first_description()
            else:
                return "Error: No Result"


# if __name__ == "__main__":
#     d = DBPediaAPI()
#     print(d.search("cwru"))