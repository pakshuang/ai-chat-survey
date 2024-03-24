import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from openai import OpenAI


class LLM(ABC):
    '''
    A large language model class. 
    Supports extension to other APIs/other LLM types such as local open-source LLMs.
    '''
    @abstractmethod
    def run(self, messages: list) -> str:
        pass


class GPT(LLM):
    '''
    Wrapper class around GPT-4 from OpenAI.
    '''
    def __init__(self, model="gpt-4"):
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.client = client
        self.model = model
        super().__init__()

    def run(self, messages: list) -> str:
        output = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )
        return output.choices[0].message.content

class ChatLog: 
    '''
    A simple wrapper around a list of messages that supports the deletion of future messages.
    '''

    SYSPROMPT = """You are an assistant who is trying to gather user responses for a product.
        You have collected some survey responses, and you would like to probe further about what the user thinks about the product.
        The user responses are provided below. Given these responses, pretend you are an interview and please generate a question for the user.
        After the user replies, decide if you wish to probe further, ask other questions regarding the user's survey responses, or thank the user and end the conversation when you have learnt enough.
        {survey_initial_responses}"""

    def __init__(self, message_list: list[dict[str, str]]):
        self.message_list = message_list
        self.current_index = len(message_list)

    def insert_and_update(self, message: str, index: int, is_llm: bool = False) -> list:
        """
        Add a new reply to the conversation chain. If edits are made in the middle, future conversations are deleted.
        Returns a message list.
        """
        if is_llm:
            role = "assistant"
        else:
            role = "user"

        self.message_list.insert(index, {"role": role, "content": message})
        self.current_index = index + 1
        self.message_list = self.message_list[: self.current_index]
        return self.message_list

def construct_chatlog(survey_initial_responses: str) -> ChatLog:
    start_dict = {
            "role": "system",
            "content": ChatLog.SYSPROMPT.format(
                survey_initial_responses=survey_initial_responses
            ),
        }
    return ChatLog([start_dict])


if __name__ == "__main__":
############### TEST HERE ######################
###### This should be moved to test folder #####
    string = """
    1. What do you like about colgate toothpaste?
    Tastes okay, makes teeth feel good
    2. Would you recommend it to a friend?
    No
    3. What do you think about colgate toothbrushes?
    Useful, durable, does not break.
    4. Would you recommend it to a friend?
    Yes
    5. Do you have any friends or family working at Colgate?
    No.
    6. What do you think about the taste of colgate toothpaste?
    It is very bitter and disgusting.
    7. How often do you consumer sweet drinks?
    Every day.
    """
    llm = GPT()
    pipe = construct_chatlog(string)

    for i in range(10):
        output = (llm.run(pipe.message_list))
        print(output)
        pipe.insert_and_update(output, pipe.current_index, is_llm=True) 
        pipe.insert_and_update(input(), pipe.current_index, is_llm=False)
    
