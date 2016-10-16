import requests

class DBPediaAPI:

    def __init__(self):
        self.keywords

    def search(self, keyword): # => json_response
        uri_string = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + keyword
        headers = {'Accept': 'application/json'}
        response = requests.get(url=uri_string, headers=headers)
        return response.json()
