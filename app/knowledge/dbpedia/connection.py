import requests
def search(keyword): # => json_response
    uri_string = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + keyword
    headers = {'Accept': 'application/json'}
    response = requests.get(url=uri_string, headers=headers)
    print(response.json())
    return response.json()

if __name__ == "__main__":
    search("waterfall model")