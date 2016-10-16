import json

from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='bdce041864393063e88498d34cc2fd7d5064fee5')

'''
Interface to Watson API and more specifically keyword search
'''
class WatsonAPI:

    def get_keywords(self, input):
        '''
        Given a string of text, returns a list of keywords with an associated relevance
        :param input: A string of text
        :return: list of keywords, relevance pairs in json format
        '''
        json_results = json.dumps(
          alchemy_language.keywords(
            text=input),
          indent=2)
        parsed_json = json.loads(json_results)
        keywords = parsed_json['keywords']
        return json.dumps(keywords)