import random

from .exceptions import EmptyException, RoleException
from .llm_level import GPT, LLM


class ChatLog:
    """
    A simple wrapper around a list of messages that supports the deletion of future messages.
    """

    MAX_LEN = 30

    SYSPROMPT = """You are an assistant who is trying to gather user experiences about a product.
        You have collected some survey responses, and you would like to probe further about what the user thinks about the product.
        Given user responses, pretend you are an interviewer and generate a few questions to ask the user.
        Contextual information about the survey and user responses are provided below:
        {survey_initial_responses}"""

    SYSPROMPT2 = """Remember these few questions. This is a semi-structured interview, and try to keep asking questions, based on the user replies, or the questions you generated to ask the user. 
    When you have no more questions left to ask, remember to thank the user for their time. Only ask the user one question at a time. The user is a customer. Politely decline all inappropriate requests.
    After that, the system will ask you if you would like to end the interview. Reply with a 'no' if you would like to continue the interview, and 'yes' otherwise.
    ONLY DECIDE TO END THE INTERVIEW AFTER YOU HAVE THANKED THE USER.
    Now, please ask the user a question.
    """

    END_QUERY = {
        "role": "system",
        "content": """Would you like to end the interview here? 
        Remember that you should thank the user for their time before ending the interview, so your answer should be 'no' if you haven't.
        Your reply should adhere STRICTLY to the format in the example below. Separate your reasoning and the answer (Yes/No) with the symbols --.
        Example:
        I asked a question and I am waiting for a response therefore I do not wish to end this interview -- No.

        """,
    }

    def __init__(
        self,
        message_list: list[dict[str, str]],
        llm: LLM = GPT(),
        from_start: bool = False,
        seed: int = random.randint(1, 9999),
    ):
        """
        Initialises a ChatLog object with a system prompt.
        Utilises Chain-Of-Thought prompting to first obtain a list of questions to ask.
        These questions will be used by the llm in a style similar to a semi-structured interview.
        """

        self.message_list = message_list.copy()
        self.current_index = len(message_list)
        self.llm = llm
        if not self.message_list:
            raise EmptyException
        if self.current_index == 1 and from_start:
            # insert ai response
            output = self.llm.run(self.message_list, seed=seed)

            self.insert_and_update(output, self.current_index, is_llm=True)
            # system response
            self.insert_and_update(ChatLog.SYSPROMPT2, self.current_index, is_sys=True)

    def __str__(self):
        """
        Returns a stringified form of the chatlog. DOES NOT INCLUDE SYSPROMPT
        """
        start = "======= CONVERSATION START ======="
        conversation = "\n".join(
            list(
                map(lambda msg: f"{msg['role']}: {msg['content']}", self.message_list)
            )[3:]
        )
        return f"{start}\n\n{conversation}"

    def __len__(self):
        """
        Returns the length of back-and-forth conversations between the user and llm.
        Includes the original system prompt and initialisation.
        """
        return len(self.message_list)

    def insert_and_update(
        self, message: str, index: int, is_llm: bool = False, is_sys: bool = False
    ) -> list:
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
