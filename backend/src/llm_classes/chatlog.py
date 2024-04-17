import random

from .exceptions import EmptyException, RoleException
from .llm_level import GPT, LLM


class ChatLog:
    """A simple wrapper around a list of messages that supports the deletion/edits of messages.

    Raises:
        EmptyException: Thrown when ChatLog is instantiated with an empty message list.
        RoleException: Thrown when a message is inserted into the message list with multiple roles entered.

    Returns:
        _type_: A ChatLog instance.
    """

    MIN_LEN = 4  # length at initialisation
    MAX_LEN = 50
    EXIT_DELIM = "--"
    SYSPROMPT = """You are an interviewer who is trying to gather opinions and insights from the user about a particular subject.
    You have already collected some survey responses from the user.
    An interview context is provided below. This context includes background information about the subject and the user's survey responses.
    The interview context may also prescribe a persona for you to adopt during the interview, please adhere to it.
    Your task is to generate a few key questions (in the prescribed persona if provided) based on the user's responses and the interview context provided to seek clarification if needed or probe for more insights on the subject.
    Interview context:
    {survey_initial_responses}"""

    SYSPROMPT2 = """Remember these few questions. This is a semi-structured interview, and try to keep asking questions, based on the user replies, or the questions you generated to ask the user. 
    Only ask the user one question at a time and try to keep the questions interesting. Probe the user if the user shows any inconsistencies in their replies, or ask for clarifications if needed. The user is a customer, so politely decline all inappropriate requests.
    When you have no more questions left to ask, remember to thank the user for their time and tell the user you intend to end the interview. When you end the interview, there is no need to ask the user for further input.
    After that, the system will ask you if you would like to end the interview.
    ONLY SAY "YES" IF YOU HAVE THANKED THE USER FOR THEIR TIME. 
    Now, as a survey interviewer, begin the interview by asking the user a question.
    """

    END_QUERY = {
        "role": "system",
        "content": """Would you like to end the interview here? 
        Before you answer the question, remember if you have thanked the user for their time and told them you would be ending the interview. Your answer should be 'no' if you haven't done either.
        Your reply should adhere STRICTLY to the format provided below. Separate your reasoning and the answer (Yes/No) with the symbols --.
        Here are three examples.
        Example 1:
        I asked a question and I am waiting for a response therefore I do not wish to end this interview -- No.
        Example 2:
        The user seems uncooperative and I am unlikely to receive a proper response but I have not thanked the user for their time and said goodbye, so I will inform them that I wish to end the interview first. -- No.
        Example 3:
        I believe I have obtained enough information about the user's preferences regarding the product. It's now a good time to conclude this interview. However, I have not thanked the user for their time and said goodbye. I will tell thank the user for their time and inform them that the interview is over first. -- No.
        Now, please answer the question.
        """,
    }

    def __init__(
        self,
        message_list: list[dict[str, str]],
        llm: LLM = GPT(),
        from_start: bool = False,
        seed: int = random.randint(1, 9999),
    ):
        """Initialises a ChatLog object with a system prompt.
        Utilises Chain-Of-Thought prompting to first obtain a list of questions to ask.
        These questions will be used by the llm in a style similar to a semi-structured interview.

        Args:
            message_list (list[dict[str, str]]): A list of messages, or a conversation.
            llm (LLM, optional): A large language model. Defaults to gpt-4-turbo-preview.
            from_start (bool, optional): Is initalising the chatlog with multi-stage system prompting. Defaults to False.
            seed (int, optional): random seed. Defaults to a random integer from 1 to 9998.

        Raises:
            EmptyException: Thrown when the ChatLog class is instantiated with an empty message_list parameter.
        """

        self.message_list = message_list.copy()
        self.current_index = len(message_list)
        self.llm = llm
        if not self.message_list:
            raise EmptyException
        if self.current_index == 1 and from_start:
            # insert ai response
            output = self.llm.run(self.message_list, seed=seed, with_moderation=False)

            self.insert_and_update(output, self.current_index, is_llm=True)
            # system response
            self.insert_and_update(ChatLog.SYSPROMPT2, self.current_index, is_sys=True)

    def __str__(self):
        """
        Returns a stringified form of the chatlog.
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
        """Add a new reply to the conversation chain. If edits are made in the middle, future conversations are deleted.
        Returns a message list.

        Args:
            message (str): Message to insert into the list of messages.
            index (int): Index in list of messages to insert message.
            is_llm (bool, optional): Role is LLM. Defaults to False.
            is_sys (bool, optional): Role is System. Defaults to False.

        Raises:
            RoleException: Thrown when is_llm and is_sys are True.

        Returns:
            list: Updated list of messages.
        """ """"""

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
