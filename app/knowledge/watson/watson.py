import json

from watson_developer_cloud import AlchemyLanguageV1

# using backup api key
# backup to the backup 08f9e64e5df9a7dbb5d5cf2be1d0b96163b220f9
alchemy_language = AlchemyLanguageV1(api_key ='7aeac8be510b62064833c518fcf73e400bfab2c2')
# backup apikey = f03242140ef3d503e4b744ef70f33c30214894ee
# alchemy_language = AlchemyLanguageV1(api_key='6b2352eeeb11ed3e8e4cb16d874506dea64503a5')

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
