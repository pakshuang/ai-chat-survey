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

    def run(self, messages: list) -> str:
        output = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )
        return output.choices[0].message.content
    
class RoleException(Exception):
    '''
    Raised when choosing multiple roles.
    '''
    def __init__(self) -> None:
        self.message = "Cannot be both assistant and llm!"
        super().__init__(self.message)


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
    When you have no more questions left to ask, remember to thank the user for their time. Only ask the user one question at a time. 
    After that, the system will ask you if you would like to end the interview. Please reply 'yes' or 'no' only. ONLY SAY 'yes' AFTER YOU HAVE THANKED THE USER.
    Now, please ask the user a question.
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

def construct_chatlog(survey_initial_responses: str, llm: LLM = GPT()) -> ChatLog:
    start_dict = {
            "role": "system",
            "content": ChatLog.SYSPROMPT.format(
                survey_initial_responses=survey_initial_responses
            ),
        }
    return ChatLog([start_dict], llm=llm, from_start=True)

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


if __name__ == "__main__":
############### TEST HERE ######################
###### This should be moved to test folder #####
    string = """
This survey is for Apple, the software company.
We are conducting a survey for the iphone 69, a new model for the Iphone.


How satisfied are you with our product/service?

Options:
-    Very satisfied
-    Satisfied
-    Neutral
-    Dissatisfied
-    Very dissatisfied
Answer: Satisfied
How likely are you to recommend our product/service to others?

-   Very likely
-   Likely
-   Neutral
-   Unlikely
-   Very unlikely

Answer: Very likely
On a scale of 1 to 10, how would you rate the quality of our product/service?

Answer: 8
What do you like most about our product/service?

Answer: The ease of use and reliability.
What improvements would you suggest for our product/service?

Answer: More customization options and faster response times.
How often do you use our product/service?

-    Daily
-    Weekly
-    Monthly
-    Occasionally
-    Rarely
Answer: Weekly
How satisfied are you with the customer support provided?
Options:
-    Very satisfied
-    Satisfied
-    Neutral
-    Dissatisfied
-    Very dissatisfied
Answer: Satisfied
What made you choose our product/service over competitors?

Answer: Positive reviews and reputation.
How would you rate the value for money of our product/service?

Answer: 7
How easy was it to purchase/use our product/service?
Options:
-    Very easy
-    Easy
-    Neutral
-    Difficult
-    Very difficult
Answer: Easy
Would you consider purchasing from us again in the future?
Options:
-    Yes
-    No
-    Maybe
Answer: Yes
Overall, how satisfied are you with your experience with our company?
Options:
-    Very satisfied
-    Satisfied
-    Neutral
-    Dissatisfied
-    Very dissatisfied
Answer: Very satisfied
What improvements would you like to see in our company as a whole?

Answer: More frequent updates and better communication with customers.
How did you first hear about our company?
Options:
-    Word of mouth
-    Online advertisement
-    Social media
-    Other (please specify)

Answer: Word of mouth
Additional Comments:
Answer: Keep up the good work!


    """
    llm = GPT()
    pipe = construct_chatlog(string, llm=llm)
    import re
    for i in range(100):
        output = (llm.run(pipe.message_list))
        print(output)     
        pipe.insert_and_update(output, pipe.current_index, is_llm=True) 

        bye = pipe.message_list.copy()
        bye.append(
            ChatLog.END_QUERY
        )
        result = llm.run(bye)
        if re.search(r"[yY]es", result):
            break

        pipe.insert_and_update(input(), pipe.current_index, is_llm=False)

    print(pipe)
    



   