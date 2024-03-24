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

    SYSPROMPT = """You are an assistant who is trying to gather user experiences about a product.
        You have collected some survey responses, and you would like to probe further about what the user thinks about the product.
        The user responses are provided below. Given these responses, pretend you are an interviewer and generate a few questions to ask the user.
        {survey_initial_responses}"""

    SYSPROMPT2 = """Remember these few questions. Now generate one and only one question for the user. Try to keep asking questions. 
    When you have no more questions left to ask, remember to thank the user by saying "Thank you and goodbye!". 
    The system will ask you if you have any more questions, to which you will say 'no' if you are finished with the interview, or 'yes' if you have more questions."""
    
    END_QUERY = {
                "role": "system",
                "content": "Do you have any more questions for the user?"
                }

    def __init__(self, message_list: list[dict[str, str]], llm: LLM = GPT()):
        self.message_list = message_list
        self.current_index = len(message_list)
        self.llm = llm
        if self.current_index == 1:
            # insert ai response
            output = self.llm.run(self.message_list)
            
            self.insert_and_update(output, self.current_index, is_llm=True) 
            # system response
            self.insert_and_update(ChatLog.SYSPROMPT2, self.current_index, is_sys=True)
            # output = self.llm.run(self.message_list)
            # self.insert_and_update(output, self.current_index, is_llm=True) 

           


    def insert_and_update(self, message: str, index: int, is_llm: bool = False, is_sys: bool = False) -> list:
        """
        Add a new reply to the conversation chain. If edits are made in the middle, future conversations are deleted.
        Returns a message list.
        """
        if is_llm and is_sys:
            raise Exception("Double roles!")
        
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

def construct_chatlog(survey_initial_responses: str) -> ChatLog:
    start_dict = {
            "role": "system",
            "content": ChatLog.SYSPROMPT.format(
                survey_initial_responses=survey_initial_responses
            ),
        }
    return ChatLog([start_dict])

def format_responses_for_gpt(response: dict[str, object]) -> str:
        '''
        Converts a response dictionary object into a string of questions and answers.
        '''
        answers = response["answers"]
        formatted = list(
            map(
                lambda ans: f"{ans["question_id"]}. {ans["question"]}\n{ans["answer"]}", answers
            )

        )
        return "\n".join(formatted)   


if __name__ == "__main__":
############### TEST HERE ######################
###### This should be moved to test folder #####
    string = """
    
How satisfied are you with your overall experience using the iPhone 15?

Answer: Very satisfied, it exceeded my expectations.
What features of the iPhone 15 do you find most appealing?

Answer: I love the upgraded camera quality and the faster processor.
On a scale of 1 to 5, how would you rate the battery life of the iPhone 15?

Answer: 4, it lasts significantly longer compared to my previous phone.
How would you rate the design and aesthetics of the iPhone 15?

Answer: 5, it's sleek and stylish.
Have you encountered any issues or drawbacks while using the iPhone 15? If yes, please specify.

Answer: No, I haven't encountered any major issues so far.
How likely are you to recommend the iPhone 15 to a friend or family member?

Answer: 9, I would highly recommend it.
What improvements would you like to see in future versions of the iPhone?

Answer: Maybe even longer battery life and more customization options.
How satisfied are you with the performance and speed of the iPhone 15?

Answer: 5, it's incredibly fast and responsive.
Do you find the features of the iPhone 15 intuitive and easy to use?

Answer: Yes, the interface is user-friendly.
How would you rate the camera quality of the iPhone 15 for both photos and videos?

Answer: 5, the camera quality is exceptional.
What made you choose the iPhone 15 over other smartphone options?

Answer: I trust the reliability and quality of Apple products.
Are there any specific apps or functions on the iPhone 15 that you find particularly useful or enjoyable?

Answer: I love using FaceTime and the various photography features.
How satisfied are you with the display quality and resolution of the iPhone 15?

Answer: 5, the display is crisp and vibrant.
Have you experienced any connectivity issues with the iPhone 15 (e.g., Wi-Fi, Bluetooth)?

Answer: No, connectivity has been smooth.
Would you consider upgrading to future iPhone models based on your experience with the iPhone 15?

Answer: Yes, if they continue to innovate and improve like they did with this model.

    """
    llm = GPT()
    pipe = construct_chatlog(string)
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
        if re.search(r"[nN]o", result):
            break

        pipe.insert_and_update(input(), pipe.current_index, is_llm=False)
    



   