from llm_classes.llm_level import LLM, GPT
from llm_classes.chatlog import ChatLog
import random

def construct_chatlog(survey_initial_responses: str, llm: LLM = GPT(), seed=random.randint(1, 9999)) -> ChatLog:
    start_dict = {
            "role": "system",
            "content": ChatLog.SYSPROMPT.format(
                survey_initial_responses=survey_initial_responses
            ),
        }
    return ChatLog([start_dict], llm=llm, from_start=True, seed=seed)

def format_responses_for_gpt(response: dict[str, object]) -> str:
        '''
        Converts a response dictionary object into a string of questions and answers.
        '''
        answers = response["answers"]
        formatted = list(
            map(
                lambda ans: f'{ans["question_id"]}. {ans["question"]}\n{ans["answer"]}', answers
            )

        )
        return "\n".join(formatted)   






   