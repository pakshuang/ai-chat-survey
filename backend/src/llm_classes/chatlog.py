from llm_classes.llm_level import LLM, GPT, RoleException

class ChatLog: 
    '''
    A simple wrapper around a list of messages that supports the deletion of future messages.
    '''
    MAX_LEN = 30

    SYSPROMPT = """You are an assistant who is trying to gather user experiences about a product.
        You have collected some survey responses, and you would like to probe further about what the user thinks about the product.
        Given user responses, pretend you are an interviewer and generate a few questions to ask the user.
        Contextual information about the survey and user responses are provided below:
        {survey_initial_responses}"""

    SYSPROMPT2 = """Remember these few questions. This is a semi-structured interview, and try to keep asking questions, based on the user replies, or the questions you generated to ask the user. 
    When you have no more questions left to ask, remember to thank the user for their time. Only ask the user one question at a time. The user is a customer. Politely decline all inappropriate requests.
    After that, the system will ask you if you would like to end the interview. Please reply 'yes' or 'no' only. ONLY SAY 'yes' AFTER YOU HAVE THANKED THE USER.
    Now, please greet the user and ask a question.
    """
    
    END_QUERY = {
                "role": "system",
                "content": """Would you like to end the interview here? If you have not thanked the user, please say 'no'. 
                If you have more questions to ask the user, or if the user has not replied, please also say 'no'. """
                }

    def __init__(self, message_list: list[dict[str, str]], llm: LLM = GPT(), from_start: bool=False):
        self.message_list = message_list.copy()
        self.current_index = len(message_list)
        self.llm = llm
        if self.current_index == 1 and from_start:
            # insert ai response
            output = self.llm.run(self.message_list)
            
            self.insert_and_update(output, self.current_index, is_llm=True) 
            # system response
            self.insert_and_update(ChatLog.SYSPROMPT2, self.current_index, is_sys=True)
      

    def __str__(self):
        '''
        Returns a stringified form of the chatlog. DOES NOT INCLUDE SYSPROMPT
        '''
        start = "======= CONVERSATION START ======="
        conversation = "\n".join(
            list(
                map(
            lambda msg: f"{msg['role']}: {msg['content']}", self.message_list
                )
            )[3:]
        )
        return f"{start}\n\n{conversation}"
    
    def __len__(self):
        return len(self.message_list) - 3   


    def insert_and_update(self, message: str, index: int, is_llm: bool = False, is_sys: bool = False) -> list:
        """
        Add a new reply to the conversation chain. If edits are made in the middle, future conversations are deleted.
        Returns a message list.
        """
        if is_llm and is_sys:
            raise RoleException()
        if is_llm:
            role = "assistant"
        elif is_sys:
            role = "system"
        else:
            role = "user"

        self.message_list.insert(index, {"role": role, "content": message})
        self.current_index = index + 1
        self.message_list = self.message_list[: self.current_index]
        return self.message_list