import requests
import json

class DBPediaAPI:

    def search(self, keyword): # => json_response
        uri_string = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + keyword
        headers = {'Accept': 'application/json'}
        response = requests.get(url=uri_string, headers=headers)
        return response.json()
#
# if __name__ == "__main__":
#     d = DBPediaAPI()
#     print(d.search("agile model"))