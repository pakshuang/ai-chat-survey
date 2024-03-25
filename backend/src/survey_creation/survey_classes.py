import json

class SurveyLoadException(Exception):
    '''
    Raised when loading into json fails.
    '''
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class Question:
    
    def __init__(self, id: str, type: str, question: str, options: str):
        self.id = id
        self.type = type
        self.question = question
        self.options = options
        self.answer = None

    def is_complete(self):
        return self.answer is None
        

    def question_as_dict(self) -> dict[str, object]:
        '''
        Returns a question.
        '''
        return {
            "id": self.id,
            "type": self.type,
            "question": self.question,  
            "options": self.options 
        }
    
    def answers_as_dict(self) -> dict[str, object]:
        '''
        Returns a question-answer.
        '''
        if not self.is_complete():
            raise Exception("Rese not complete!")
        else:
            return {
            "question_id": self.id,
            "type": self.type, 
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
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