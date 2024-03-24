import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from openai import OpenAI


class LLM(ABC):
    @abstractmethod
    def run(self, messages: list) -> str:
        pass


class GPT(LLM):
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
