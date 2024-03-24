from llm_level import *


class ChatLog:
    
    '''
    A simple wrapper around a list of messages that supports the deletion of future messages.
    '''

    SYSPROMPT = """You are an assistant who is trying to gather user responses for a product.
        You have collected some survey responses, and you would like to probe further about what the user thinks about the product.
        The user responses are provided below. Given these responses, pretend you are an interview and please generate one and only one question for the user.
        {survey_initial_responses}"""

    def __init__(self, survey_initial_responses: str, start_items=1):
        start_dict = {
            "role": "system",
            "content": ChatLog.SYSPROMPT.format(
                survey_initial_responses=survey_initial_responses
            ),
        }

        self.message_list = [start_dict]
        self.current_index = 1

    def insert_and_update(self, message: str, index: int, is_llm: bool) -> list:
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


################ TEST HERE ######################
# string = """
# 1. What do you like about colgate toothpaste?
# Tastes okay, makes teeth feel good
# 2. Would you recommend it to a friend?
# No
# """
# llm = GPT()
# pipe = ChatLog(string)
# print(llm.run(pipe.message_list))
