import os
import random
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from openai import OpenAI
from peft import AutoPeftModelForCausalLM
import torch
from transformers import AutoTokenizer

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
            model=self.model,
            messages=messages,
            stream=False,
            temperature=0.4,
            top_p=0.4,
            seed=seed,
        )
        output_text = output.choices[0].message.content
        if with_moderation and self.content_moderation.is_harmful(output_text):
            return self.content_moderation.default
        else:
            return output_text


class LocalLLMGPTQ(LLM):

    """A class for GPTQ-quantised LLM"""

    def __init__(self):
        self.path = "../models/"
        model = AutoPeftModelForCausalLM.from_pretrained(
            self.path,
            low_cpu_mem_usage=True,
            return_dict=True,
            torch_dtype=torch.float16,
            device_map="cuda",
        )

        tokenizer = AutoTokenizer.from_pretrained(self.path + "/dolphin-2.2.1-mistral-7B-GPTQ/")
        self.model, self.tokenizer = model, tokenizer

    def run(
        self, messages: list, seed: int = random.randint(1, 9999), with_moderation=True
    ):
        """Runs the llm given a current conversation and seed and outputs a string.

        Args:
            messages (list): A list of messages tied to a ChatLog instance.
            seed (int, optional): A random integer. Defaults to a random integer from 1 to 9998.
            with_moderation (bool, optional): Whether to activate moderation module to filter content. Defaults to True.

        Returns:
            str: text output from the Large Language Model.
        """
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
