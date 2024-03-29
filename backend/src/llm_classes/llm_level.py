import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from openai import OpenAI
import random

class LLM(ABC):
    '''
    A large language model class. 
    Supports extension to other APIs/other LLM types such as local open-source LLMs.
    '''
    @abstractmethod
    def run(self, messages: list) -> str:
        return

class GPT(LLM):
    '''
    Wrapper class around the GPT models from OpenAI.
    '''
    def __init__(self, model="gpt-4"):
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.client = client
        self.model = model
        super().__init__()

    def run(self, messages: list, seed: int = random.randint(1, 9999)) -> str:
        '''
        Runs the llm given a current conversation and seed and outputs a string.
        '''
        output = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
            seed=seed
        )
        return output.choices[0].message.content
    
class RoleException(Exception):
    '''
    Raised when choosing multiple roles.
    '''
    def __init__(self):
        self.message = "Cannot be both assistant and llm!"
        super().__init__(self.message)

class EmptyException(Exception):
    '''
    Raised when a ChatLog is instantiated with an empty list.
    '''
    def __init__(self):
        self.message = "Cannot have empty message list!"
        super().__init__(self.message)