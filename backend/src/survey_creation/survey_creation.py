import json

class SurveyLoadException(Exception):
    '''
    Raised when loading into json fails.
    '''
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class Question:
    '''
    A survey question. When we feed into GPT, need to format them right.
    I suggest each type of question aka mrq, mcq be its own subtype, and we can format them differently.
    '''

    def __init__(self, id: str, type: str):
        self.id = id
        self.type = type
        

    def as_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "type": self.type
            # TO BE UPDATED
        }
    
class Survey:
    '''
    Constructs a survey. Probably client will use this when building survey.
    '''
    def __init__(
            self, metadata: dict[str, object], 
            title: str, 
            subtitle: str, 
            questions: list[Question], 
            chat_context: str):
        
        self.metadata = metadata
        self.title = title
        self.subtitle = subtitle
        self.questions = questions
        self.chat_context = chat_context

    def as_dict(self) -> dict[str, object]:
        
        return {
            "metadata": self.metadata,
            "title": self.title,
            "subtitle": self.subtitle,
            "questions": list(map(lambda question: question.as_dict(), self.questions)),
            "chat_context": self.chat_context
        }


def create_questions_from_list(questions: list[dict]) -> list[Question]:
        return list(
            map(lambda question: Question(question["id"], question["type"]), questions)
        )

def construct_survey_from_json(json_string: str) -> Survey:
    '''
    Accepts a json string in the format of a survey and returns a survey object.
    '''
    try:
        to_json = json.loads(json_string)

        survey = Survey(
            to_json['metadata'],
            to_json['title'],
            to_json['subtitle'],
            create_questions_from_list(to_json['questions']),
            to_json['survey_chat_context']
        )
        return survey
        
    except Exception as e:
        raise SurveyLoadException(e) from None