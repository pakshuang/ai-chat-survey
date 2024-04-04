import logging
import random
import re

from .chatlog import ChatLog
from .llm_level import GPT, LLM

# Custom logger
logger = logging.getLogger("exit_logger")
logger.setLevel(logging.WARNING)
file_handler = logging.FileHandler("./logs/exit_chat.log")
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def construct_chatlog(
    survey_initial_responses: str, llm: LLM = GPT(), seed: int = random.randint(1, 9999)
) -> ChatLog:
    """Given a formatted survey response, constructs a ChatLog object.

    Args:
        survey_initial_responses (str): Initial responses to the static survey.
        llm (LLM, optional): A Large Language Model object.. Defaults to gpt-4-turbo-preview.
        seed (int, optional): A random integer. Defaults to an integer from the range 1 to 9998.

    Returns:
        ChatLog: An instance of the ChatLog class.
    """
    start_dict = {
        "role": "system",
        "content": ChatLog.SYSPROMPT.format(
            survey_initial_responses=survey_initial_responses
        ),
    }
    return ChatLog([start_dict], llm=llm, from_start=True, seed=seed)


def format_multiple_choices(
    choices: list[str], title: str, sep: str = ", ", add_plural: bool = True
) -> str:
    """Formats multiple choice and multiple response options and answers in JSON format into strings.

    Args:
        choices (list[str]): Choices
        title (str): Options or Questions
        sep (str, optional): A separator between options/answers. Defaults to ", ".
        add_plural (bool, optional): Defaults to True.

    Returns:
        str: A formatted string to be passed into a LLM.
    """

    if choices and (choices[0] or len(choices) > 1):
        # there exists at least one choice that is not [""]
        if add_plural and len(choices) > 1:
            return title + "s:\n" + sep.join(choices)
        return title + ":\n" + sep.join(choices)
    elif not choices or not choices[0]:
        return ""


def format_responses_for_gpt(response: dict[str, object]) -> str:
    """Converts a response dictionary object into a string of questions and answers.

    Args:
        response (dict[str, object]): A response object converted into a dict.

    Returns:
        str: A formatted string to be passed into a LLM.
    """
    answers = response["answers"]
    formatted = list(
        map(
            lambda ans: f"""{ans["question_id"]}. {ans["question"]}\n{format_multiple_choices(ans["options"], "Option")}\n{format_multiple_choices(ans["answer"], "Answer")}""",
            answers,
        )
    )
    return "\n".join(formatted)


def check_exit(
    updated_message_list: list[dict[str, str]],
    llm: LLM,
    seed: int = random.randint(1, 9999),
    delim: str = ChatLog.EXIT_DELIM,
) -> bool:
    """Checks if the interactive survey has come to a conclusion. Returns a boolean.

    Args:
        updated_message_list (list[dict[str, str]]): A message list tied to the ChatLog instance.
        llm (LLM): A LLM object.
        seed (int, optional): An random integer controlling pseudo-randomness. Defaults to a random integer from 1 to 9998
        delim (str, optional): A delimiter to parse a formatted LLM output. Defaults to ChatLog.EXIT_DELIM, which defaults to "--".

    Returns:
        bool: _description_
    """ """
    
    """
    if len(updated_message_list) <= ChatLog.MIN_LEN:
        return False
    exit = updated_message_list.copy()
    exit.append(ChatLog.END_QUERY)
    result = llm.run(exit, seed=seed, with_moderation=False)

    is_last = bool(re.search(r"[yY]es", result.split(delim)[-1]))
    logger.warning(f"exit: {is_last}, Reasoning: {result}")
    return is_last or (len(updated_message_list) > ChatLog.MAX_LEN)
