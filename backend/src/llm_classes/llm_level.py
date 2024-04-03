import os
import random
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from openai import OpenAI


class LLM(ABC):
    """A large language model class.
    Supports extension to other APIs/other LLM types such as local open-source LLMs.
    """  #

    @abstractmethod
    def run(
        self, messages: list, seed: int = random.randint(1, 9999), with_moderation=True
    ) -> str:
        return


class ContentModeration:
    """A wrapper class around a content filter, for added security measures.
    Currently uses a model from Openai API.
    Redefine this class if the application is scaled for a larger user-base.
    """

    def __init__(self, client: OpenAI):
        self.default = "Sorry, I cannot assist you with that. Please note that your replies are being logged."
        self.client = client

    def is_harmful(self, text: str) -> bool:
        """
        Checks if text is harmful and inappropriate. Returns a boolean.

        Args:
            text (str): Text to check.

        Returns:
            bool: A boolean value that determines if the text is inappropriate.
        """
        response = self.client.moderations.create(input=text)
        return response.results[0].flagged


class GPT(LLM):
    """Wrapper class around the GPT models from OpenAI."""

    def __init__(self, model="gpt-4-turbo-preview"):
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.client = client
        self.model = model
        self.content_moderation = ContentModeration(self.client)
        super().__init__()

    def run(
        self, messages: list, seed: int = random.randint(1, 9999), with_moderation=True
    ) -> str:
        """Runs the llm given a current conversation and seed and outputs a string.

        Args:
            messages (list): A list of messages tied to a ChatLog instance.
            seed (int, optional): A random integer. Defaults to a random integer from 1 to 9998.
            with_moderation (bool, optional): Whether to activate moderation module to filter content. Defaults to True.

        Returns:
            str: text output from the Large Language Model.
        """
        output = self.client.chat.completions.create(
            model=self.model, messages=messages, stream=False, seed=seed
        )
        output_text = output.choices[0].message.content
        if with_moderation and self.content_moderation.is_harmful(output_text):
            return self.content_moderation.default
        else:
            return output_text


class LocalLLMGPTQ(LLM):
    # LOCAL-LLMS CAN BE DEFINED IN THIS CLASS SUCH THAT THE APP CAN SUPPORT LOCALLLMS
    # REQUIRES:
    # 1. THE TRANSFORMERS LIBRARY, WHICH IS NOT IMPORTED:
    #       from transformers import AutoModelForCausalLM, AutoTokenizer
    # 2. NVIDIA-GPU (With at least 8GB VRAM)
    # 3. CUDA (At least 11.8)
    # The following skeleton code will help:
    # path = "C:\..." (Where you store your model)
    # model = AutoModelForCausalLM.from_pretrained(path, device_map="cuda")
    # tokenizer = AutoTokenizer.from_pretrained(path)
    #
    """A class for GPTQ-quantised LLM"""

    def __init__(self, path):
        pass
        # model = AutoModelForCausalLM.from_pretrained(path, device_map="cuda")
        # tokenizer = AutoTokenizer.from_pretrained(path)
        # self.model, self.tokenizer = model, tokenizer

    def run(self, messages: list, seed: int = random.randint(1, 9999)):
        """Runs the llm given a current conversation and seed and outputs a string.

        Args:
            messages (list): A list of messages tied to a ChatLog instance.
            seed (int, optional): A random integer. Defaults to a random integer from 1 to 9998.
            with_moderation (bool, optional): Whether to activate moderation module to filter content. Defaults to True.

        Returns:
            str: text output from the Large Language Model.
        """
        pass
        # conversations = self.tokenizer.apply_chat_template(messages)
        # input_ids = self.tokenizer(messages, return_tensors='pt').input_ids.cuda()

        # return self.model.generate(
        # inputs=input_ids,
        # temperature=0.7,
        # do_sample=True,
        # top_p=0.95,
        # top_k=40,
        # repetition_penalty=1,
        # max_new_tokens=2048,
        # eos_token_id=bot.tok.eos_token_id,
        # )
