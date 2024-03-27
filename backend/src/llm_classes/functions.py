import json
import random
import re

from database_operations import close_connection, update_chat_log
from flask import jsonify

from llm_classes.chatlog import ChatLog
from llm_classes.llm_level import GPT, LLM


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


def format_responses_for_gpt(response: dict[str, object]) -> str:
    """
    Converts a response dictionary object into a string of questions and answers.
    """
    answers = response["answers"]
    formatted = list(
        map(
            lambda ans: f'{ans["question_id"]}. {ans["question"]}\n{ans["answer"]}',
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
    return is_last


def helper_send_message(
    llm_input: dict[str, object], data_content: str, connection, survey_id, response_id
):
    """
    Generates a response from a large language model.
    """

    def has_no_chat_log(content: str, message_list: list[dict[str, object]]) -> bool:
        return not content.strip() and not message_list

    try:
        # initialise LLM
        llm = GPT()
        chat_log_dict = json.loads(llm_input["chat_log"])
        message_list = chat_log_dict["messages"]

        has_no_chat_log = has_no_chat_log(data_content, message_list)
        if has_no_chat_log:
            pipe = construct_chatlog(
                f"""{llm_input["chat_context"]}\n{
                    format_responses_for_gpt(
                        llm_input["response_object"]
                    )
                }""",
                llm=llm,
            )
            first_question = llm.run(pipe.message_list)
            updated_message_list = pipe.insert_and_update(
                first_question, pipe.current_index, is_llm=True
            )

        else:
            pipe = ChatLog(message_list, llm=llm)
            pipe.insert_and_update(data_content, pipe.current_index)  # user input
            next_question = llm.run(pipe.message_list)
            updated_message_list = pipe.insert_and_update(
                next_question, pipe.current_index, is_llm=True
            )

        updated_chat_log = chat_log_dict.copy()
        updated_chat_log["messages"] = updated_message_list
        updated_chat_log_json = json.dumps(updated_chat_log)

        # Update the ChatLog table
        try:
            # Update the database
            update_chat_log(connection, survey_id, response_id, updated_chat_log_json)
        except Exception as e:
            return (
                jsonify({"message": "An error occurred while updating the chat log"}),
                500,
            )

        content = updated_message_list[-1]["content"]
        is_last = (
            check_exit(updated_message_list, llm)
            or len(updated_message_list) > ChatLog.MAX_LEN
        )
        close_connection(connection)
        return (
            jsonify(
                {
                    "content": content,
                    "is_last": is_last,
                    "updated_message_list": updated_message_list,
                }
            ),
            201,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error was encountered while generating a reply:"
                    + str(e)
                }
            ),
            500,
        )
