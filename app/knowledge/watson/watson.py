import json

from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='bdce041864393063e88498d34cc2fd7d5064fee5')

class WatsonAPI:
    def __init__(self):
        self.keywords = []

    def get_keywords(self, input):
        json_results = json.dumps(
          alchemy_language.keywords(
            text=input),
          indent=2)
        parsed_json = json.loads(json_results)
        keywords = parsed_json['keywords']
        for i in range (0,len(keywords)):
            print(keywords[i])

def main():
    watson = WatsonAPI()
    watson.get_keywords("In terms of our API usage, based on our extensive research, Google Cloud Speech API (GCS) is"
                        "the most advanced and most accurate commercially available cloud speech API. However, since"
                        "the GCS API is somewhat costly, we are using Google Web Speech API(GWS), which uses the same"
                        "technology behind GCS, that is free for developers if called through client side Google Chrome"
                        "Browser. We believe it’s Google’s strategy to attract more developers to use speech recognition"
                        "in their web apps, so we are taking advantage of this time when the API is offered for free. We"
                        "did comparisons on a few Natural Language Processing Systems, and we decided the entity"
                        "extraction feature offered by IBM Alchemy NLP API is the most suitable system for our use."
                        "We also choose DBPedia over Google Knowledge Graph (KG) since KG yields many irrelevant results"
                        "that might lead to confusions to our users.")

if __name__ == '__main__':
    main()