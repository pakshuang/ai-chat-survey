from llm_level import *


class Pipeline:
    SYSPROMPT = "INSERT SYSTEM PROMPT"
    START = {
        "role": "system",
        "content": SYSPROMPT
    }

    def __init__(self, message_list: list, start_items=1):
        self.message_list = [Pipeline.START]
        self.current_index = 1
        

    def insert_and_update(self, message: str, index: int, is_llm: bool):
        '''
        Add a new reply to the conversation chain. If edits are made in the middle, future conversations are deleted.
        '''
        if is_llm:
            role = "assistant"
        else:
            role = "user"

        self.message_list.insert(
            index,
            {
                "role": role,
                "content": message
            }
        )
        self.current_index = index + 1 
        self.message_list = self.message_list[:self.current_index]
        return message
    




        