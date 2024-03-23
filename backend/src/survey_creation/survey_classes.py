import json

class SurveyLoadException(Exception):
    '''
    Raised when loading into json fails.
    '''
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class Survey:
    '''
    Define survey
    '''
    def __init__(self, json_string: str):
        try:
            to_json = json.loads(json_string)
            self.metadata = to_json['metadata']
            self.title = to_json['title']
            self.subtitle = to_json['subtitle']

        except Exception as e:
            raise SurveyLoadException(e) from None
        
        pass

class Question:
    '''
    A survey question. When we feed into GPT, need to format them right.
    I suggest each type of question aka mrq, mcq be its own subtype, and we can format them differently.
    '''

    def __init__(self, json_string: str):
        pass