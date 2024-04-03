# -*- coding: utf-8 -*-
"""
    src.database_operations
    ~~~~~~~

    This module implements the helper functions that do CRUD operations
    to the database for the backend server.
"""


import json
import os
from typing import Optional, Any, List, Tuple, Dict

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from src.llm_classes.llm_level import GPT


def connect_to_mysql() -> Optional[pymysql.connections.Connection]:
    """
    Connects to a MySQL database.

    Returns:
        pymysql.connections.Connection or None: A connection object if successful, None otherwise.
    """
    # Connect to MySQL
    mysql_host = os.environ.get("API_MYSQL_HOST", "database")
    mysql_user = os.environ.get("API_MYSQL_USER", "root")
    mysql_password = os.environ.get("API_MYSQL_PASSWORD", "password")
    mysql_db = os.environ.get("API_MYSQL_DB", "ai_chat_survey_db")

    try:
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return connection
    except pymysql.Error as e:
        raise e


def get_cursor(connection: Connection) -> Cursor:
    """
    Returns a cursor object associated with the provided database connection.

    Args:
        connection: pymysql.connections.Connection object representing the database connection.

    Returns:
        pymysql.cursors.Cursor: Cursor object for executing SQL queries.
    """
    return connection.cursor()


def close_connection(connection: Connection) -> None:
    """
    Close the provided database connection if it's open.

    Args:
        connection (pymysql.connections.Connection): The database connection to be closed.
    """
    if connection:
        connection.close()


def commit(connection: Connection) -> None:
    """
    Commit the changes made to the database through the provided connection if it's open.

    Args:
        connection (pymysql.connections.Connection): The database connection used to commit changes.
    """
    if connection:
        connection.commit()


def rollback(connection: Connection) -> None:
    """
    Roll back any uncommitted changes made to the database through the provided connection if it's open.

    Args:
        connection (pymysql.connections.Connection): The database connection used to rollback changes.
    """
    if connection:
        connection.rollback()


def execute(connection: Connection, query: str, params: Optional[tuple] = None) -> None:
    """
    Execute a SQL query using the provided connection and optional parameters.

    Args:
        connection (pymysql.connections.Connection): The database connection to execute the query.
        query (str): The SQL query to execute.
        params (tuple, optional): Optional parameters to be used in the query (default is None).
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            commit(connection)  # Commit changes after successful execution
    except Exception as e:
        # Roll back changes if execution fails
        rollback(connection)
        raise e


def fetch(connection: Connection, query: str, params: Optional[tuple] = None) -> List[dict]:
    """
    Execute a SQL query using the provided connection and optional parameters, and fetch all results.

    Args:
        connection (pymysql.connections.Connection): The database connection to execute the query.
        query (str): The SQL query to execute.
        params (tuple, optional): Optional parameters to be used in the query (default is None).

    Returns:
        List[dict]: A list of dictionaries representing the fetched results.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        raise e


def close_cursor(cursor: Cursor) -> None:
    """
    Close the provided cursor if it's open.

    Args:
        cursor (pymysql.cursors.Cursor): The cursor to be closed.
    """
    if cursor:
        cursor.close()


# Helper functions for insertion and creation


# create_survey
def summarise(chat_context: str) -> str:
    """
    Summarize the provided chat context text.

    Args:
        chat_context (str): The text to be summarized.

    Returns:
        str: The summarized text, with a maximum length of 1500 characters.
    """
    MAX_LEN = 1500
    if len(chat_context) > MAX_LEN:
        llm = GPT()
        output = llm.run(
            [
                {
                    "role": "system",
                    "content": "You are an assistant who summarises text.",
                },
                {
                    "role": "user",
                    "content": f"""The following text will supply contextual knowledge needed for a survey. 
             Summarise it in less than 5 sentences, paying attention to what the survey is about and/or the product: 
             {chat_context}""",
                },
            ]
        )
        output = output[:MAX_LEN]
        return output
    else:
        return chat_context


def validate_survey_object(data: dict) -> Tuple[bool, str]:
    """
    Validate a survey object to ensure it follows a specific format.

    Args:
        data (dict): The survey object to validate.

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating whether the survey object is valid
                         and a message describing the result.
    """
    if not isinstance(data, dict):
        return False, "Survey data must be a dictionary"

    required_keys = ["metadata", "title", "subtitle", "questions", "chat_context"]
    for key in required_keys:
        if key not in data or not data[key]:
            return False, f"Missing or empty '{key}' field"

    if not isinstance(data["questions"], list):
        return False, "Questions field must be a list"

    for question in data["questions"]:
        required_question_keys = ["question_id", "type", "question", "options"]
        for key in required_question_keys:
            if key not in question:
                return False, f"Missing or empty '{key}' field in a question"
            elif key == "type":
                if question[key] not in [
                    "multiple_choice",
                    "multiple_response",
                    "free_response",
                ]:
                    return False, f"Invalid question type"

        if not isinstance(question["options"], list):
            return False, "Options field in a question must be a list"

    return True, "Survey object format is valid"


def create_survey(connection: Connection, data: dict) -> int:
    """
    Create a new survey in the database based on the provided survey data.

    Args:
        connection (pymysql.connections.Connection): The database connection.
        data (dict): The survey data to be inserted into the database.

    Returns:
        int: The ID of the newly created survey.
    """
    try:
        # Insert survey data into Surveys table
        insert_survey_query = """
            INSERT INTO Surveys (title, subtitle, admin_username, created_at, chat_context)
            VALUES (%s, %s, %s, %s, %s)
        """
        survey_data = (
            data["title"],
            data["subtitle"],
            data["metadata"]["created_by"],
            data["metadata"]["created_at"],
            summarise(data["chat_context"]),
        )
        cursor = connection.cursor()
        cursor.execute(insert_survey_query, survey_data)

        # Get the ID of the inserted survey
        survey_id = cursor.lastrowid

        # Insert questions into Questions table
        for question in data["questions"]:
            insert_question_query = """
                INSERT INTO Questions (question_id, survey_id, question, question_type, options)
                VALUES (%s, %s, %s, %s, %s)
            """
            question_data = (
                question["question_id"],
                survey_id,
                question["question"],
                question["type"],
                (
                    json.dumps(question.get("options", []))
                    if "options" in question
                    else None
                ),
            )
            cursor.execute(insert_question_query, question_data)

        # Commit changes and close cursor
        connection.commit()
        cursor.close()

        return survey_id
    except Exception as e:
        raise e


# get_surveys()
# Helper function to create survey object
def create_survey_object(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a survey object based on a database row.

    Args:
        row (Dict[str, Any]): The database row containing survey information.

    Returns:
        Dict[str, Any]: A dictionary representing the survey object.
    """
    survey_object = {
        "metadata": {
            "survey_id": row["survey_id"],
            "created_by": row["admin_username"],
            "created_at": row["created_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Convert to string
        },
        "title": row["title"],
        "subtitle": row["subtitle"],
        "questions": [],
        "chat_context": row["chat_context"],
    }
    return survey_object


# get_surveys()
# Helper function to create survey object
def append_question_to_survey(survey_objects: Dict[int, dict], survey_id: int, question_data: dict) -> None:
    """
    Append a question to the survey object identified by the provided survey ID.

    Args:
        survey_objects (Dict[int, dict]): A dictionary containing survey objects indexed by survey ID.
        survey_id (int): The ID of the survey to which the question will be appended.
        question_data (dict): The data of the question to be appended to the survey.

    Returns:
        None
    """
    # If the question does not exist, append it to the list
    survey_objects[survey_id]["questions"].append(
        {
            "question_id": question_data["question_id"],
            "type": question_data["question_type"],
            "question": question_data["question"],
            "options": (
                json.loads(question_data["options"]) if question_data["options"] else []
            ),
        }
    )


# submit_response()
# Helper function to insert response data into DB
def save_response_to_database(connection, data, survey_id):
    try:
        query = """
        SELECT MAX(response_id) FROM Survey_Responses WHERE survey_id = %s
        """

        # Execute the query with the survey ID as a parameter
        result = fetch(connection, query, (survey_id,))

        # If there are no results or the result is None, return 1
        if not result or result[0]["MAX(response_id)"] is None:
            last_response_id = 0
        else:
            # Extract the last response ID and return it
            last_response_id = result[0]["MAX(response_id)"]

        # Increment the last response_id by 1 to generate a new response_id
        new_response_id = last_response_id + 1

        # Save each question's response to the database
        for answer in data["answers"]:
            survey_id = data["metadata"]["survey_id"]
            question_id = answer["question_id"]
            answer_text = json.dumps(answer["answer"]) if "options" in answer else None

            # Insert the survey response into the database with the new_response_id
            query = """
                INSERT INTO Survey_Responses (response_id, survey_id, question_id, answer, submitted_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            params = (new_response_id, survey_id, question_id, answer_text)
            execute(connection, query, params)

        # Commit the transaction
        connection.commit()

        return new_response_id
    except Exception as e:
        return e


def validate_response_object(response_data):
    if not isinstance(response_data, dict):
        return False, "Response data must be a dictionary"

    if "metadata" not in response_data or "answers" not in response_data:
        return False, "Response data must contain 'metadata' and 'answers' keys"

    if not isinstance(response_data["metadata"], dict):
        return False, "'metadata' must be a dictionary"

    if "survey_id" not in response_data["metadata"]:
        return False, "'metadata' must contain 'survey_id' key"

    if not isinstance(response_data["answers"], list):
        return False, "'answers' must be a list"

    for answer in response_data["answers"]:
        if not isinstance(answer, dict):
            return False, "Each answer must be a dictionary"

        keys = ["question_id", "type", "question", "options", "answer"]
        for key in keys:
            if key not in answer:
                return False, f"Each answer must contain '{key}' key"
            elif key == "type":
                if answer[key] not in [
                    "multiple_choice",
                    "multiple_response",
                    "free_response",
                ]:
                    return False, f"Invalid question type"

        if not isinstance(answer["question_id"], int):
            return False, "'question_id' must be an integer"

        if not isinstance(answer["type"], str):
            return False, "'type' must be a string"

        if not isinstance(answer["question"], str):
            return False, "'question' must be a string"

        if not isinstance(answer["options"], list):
            return False, "'options' must be a list"

        if not isinstance(answer["answer"], list):
            return False, "'answer' must be a list"
        elif not answer["answer"]:
            return False, "'answer' is empty"

    return True, "Response object format is valid"


# submit_response()
# Helper function to validate response data structure
def validate_response(response_data, survey_object):
    response_questions = response_data.get("answers", [])
    survey_questions = survey_object.get("questions", [])

    # Check if the number of questions match
    if len(response_questions) != len(survey_questions):
        return "Number of questions in response does not match survey"

    # Iterate through each question in the response
    for response_question in response_questions:
        # Find the corresponding question in the survey
        matching_survey_question = next(
            (
                question
                for question in survey_questions
                if question["question_id"] == response_question["question_id"]
            ),
            None,
        )
        if not matching_survey_question:
            return f"Question with ID {response_question['question_id']} not found in survey"

        # Check if the type matches
        if response_question["type"] != matching_survey_question["type"]:
            return f"Question type mismatch for question with ID {response_question['question_id']}"

        # Check if the question matches
        if response_question["question"] != matching_survey_question["question"]:
            return f"Question text mismatch for question with ID {response_question['question_id']}"

        # If the question type is 'multiple_choice', check if the options match
        if response_question["type"] == "multiple_choice":
            # Check if the number of options match
            if len(response_question.get("options", [])) != len(
                matching_survey_question.get("options", [])
            ):
                return f"Number of options mismatch for question with ID {response_question['question_id']}"
            # Check if each option in the response exists in the survey question's options
            for option in response_question.get("options", []):
                if option not in matching_survey_question.get("options", []):
                    return f"Option '{option}' not found in question with ID {response_question['question_id']}'s options"

    # If all checks pass, the response object is valid
    return None


# get_responses()
# Helper method create response_object()
def create_response_object(survey_id, response_id, row):
    response_object = {
        "metadata": {
            "survey_id": int(survey_id),
            "response_id": response_id,
            "submitted_at": row["submitted_at"].strftime("%Y-%m-%d %H:%M:%S"),
        },
        "answers": [],
    }
    return response_object


# get_responses()
# Helper function to create response object
def append_answer_to_response(response_objects, response_id, response_data):
    answer = {
        "question_id": response_data["question_id"],
        "type": response_data["question_type"],
        "question": response_data["question"],
        "options": (
            json.loads(response_data["options"]) if response_data["options"] else []
        ),
        "answer": (
            json.loads(response_data["answer"]) if response_data["answer"] else []
        ),
    }
    response_objects[response_id]["answers"].append(answer)


# send_chat_message()
# Helper function to fetch the chat_context from Surveys
def fetch_chat_context(connection, survey_id):
    try:
        # Fetch chat context from the database
        chat_context_query = """
        SELECT chat_context FROM Surveys WHERE survey_id = %s
        """
        result = fetch(connection, chat_context_query, (survey_id,))
        # Check if chat context exists
        if not result:
            raise

        # If chat context exists, return it
        result = result[0]["chat_context"]
        return result
    except Exception as e:
        raise e


# send_chat_message()
# Helper function to get the chatLog or create a new chatLog
def get_chat_log(connection, survey_id, response_id):
    try:
        # Check if chat log exists for the survey
        chat_log_query = """
        SELECT chat_log FROM ChatLog WHERE survey_id = %s AND response_id = %s
        """
        result = fetch(connection, chat_log_query, (survey_id, response_id))

        # If chat log doesn't exist, create a new chat_log
        if not result:
            insert_chat_log_query = """
            INSERT INTO ChatLog (survey_id, response_id, chat_log, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """
            # Define the initial chat log structure
            initial_chat_log = {"messages": []}
            initial_chat_log = json.dumps(initial_chat_log)
            execute(
                connection,
                insert_chat_log_query,
                (survey_id, response_id, initial_chat_log),
            )
            chat_log = initial_chat_log
        else:
            chat_log = result[0]["chat_log"]

        return chat_log  # Return chat log

    except Exception as e:
        raise e


# send_chat_message()
# Helper function update chat log
def update_chat_log(connection, survey_id, response_id, updated_chat_log):
    try:
        # Update chat_log in the database
        update_chat_log_query = """
        UPDATE ChatLog SET chat_log = %s WHERE survey_id = %s AND response_id = %s
        """
        execute(
            connection,
            update_chat_log_query,
            (updated_chat_log, survey_id, response_id),
        )

        return True
    except Exception as e:
        raise e
