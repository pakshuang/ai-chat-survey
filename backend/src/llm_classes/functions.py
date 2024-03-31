import random
import re

from .chatlog import ChatLog
from .llm_level import GPT, LLM


def construct_chatlog(
    survey_initial_responses: str, llm: LLM = GPT(), seed=random.randint(1, 9999)
) -> ChatLog:
    """
    Given a formatted survey response, constructs a ChatLog object.
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

    if choices and (choices[0] or len(choices) > 1):
        # there exists at least one choice that is not [""]
        if add_plural and len(choices) > 1:
            return title + "s:\n" + sep.join(choices)
        return title + ":\n" + sep.join(choices)
    elif not choices or not choices[0]:
        return ""


def format_responses_for_gpt(response: dict[str, object]) -> str:
    """
    Converts a response dictionary object into a string of questions and answers.
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
) -> bool:
    """
    Checks if the interactive survey has come to a conclusion. Returns a boolean.
    """
    exit = updated_message_list.copy()
    exit.append(ChatLog.END_QUERY)
    result = llm.run(exit, seed=seed)
    is_last = bool(re.search(r"[yY]es", result))
    return is_last or (len(updated_message_list) > ChatLog.MAX_LEN)
