import os
import pymysql
import json


def connect_to_mysql():
    # Connect to MySQL
    mysql_host = os.getenv("MYSQL_HOST", "database")
    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_password = os.getenv("MYSQL_PASSWORD", "password")
    mysql_db = os.getenv("MYSQL_DB", "ai_chat_survey_db")

    try:
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db,
            cursorclass=pymysql.cursors.DictCursor,
        )
        print("Connected to MySQL database successfully!")
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None


def get_cursor(connection):
    return connection.cursor()


def close_connection(connection):
    if connection:
        connection.close()


def commit(connection):
    if connection:
        connection.commit()


def rollback(connection):
    if connection:
        connection.rollback()


def execute(connection, query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            commit(connection)  # Commit changes after successful execution
    except Exception as e:
        print(f"Error executing query: {e}")
        rollback(connection)  # Rollback changes in case of error


def fetch(connection, query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching results: {e}")
        return None  # Return None in case of error


def close_cursor(cursor):
    if cursor:
        cursor.close()


# Helper functions for insertion and creation

# create_survey

def create_survey(connection, data):
    try:
        # Insert survey data into Surveys table
        insert_survey_query = """
            INSERT INTO Surveys (name, description, title, subtitle, admin_username, created_at, chat_context)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        survey_data = (
            data['metadata']['name'],
            data['metadata']['description'],
            data['title'],
            data['subtitle'],
            data['metadata']['created_by'],
            data['metadata']['created_at'],
            data['chat_context']
        )
        cursor = connection.cursor()
        cursor.execute(insert_survey_query, survey_data)

        # Get the ID of the inserted survey
        survey_id = cursor.lastrowid

        # Insert questions into Questions table
        for question in data['questions']:
            insert_question_query = """
                INSERT INTO Questions (question_id, survey_id, question, question_type, options)
                VALUES (%s, %s, %s, %s, %s)
            """
            question_data = (
                question['id'],
                survey_id,
                question['question'],
                question['type'],
                json.dumps(question.get('options', [])) if 'options' in question else None
            )
            cursor.execute(insert_question_query, question_data)

        # Commit changes and close cursor
        connection.commit()
        cursor.close()

        return survey_id
    except Exception as e:
        print(f"Error creating survey: {e}")
        connection.rollback()
        return None


# get_surveys()
# Helper function to create survey object
def create_survey_object(row, questions=[]):
    survey_object = {
        "metadata": {
            "id": row['survey_id'],
            "name": row['name'],
            "description": row['description'],
            "created_by": row['admin_username'],
            "created_at": row['created_at'].strftime("%Y-%m-%d %H:%M:%S"),  # Convert to string
        },
        "title": row['title'],
        "subtitle": row['subtitle'],
        "questions": questions,  # Include questions list
        "chat_context": row['chat_context']
    }
    return survey_object

# get_surveys()
# Helper function to create survey object
def append_question_to_survey(survey_objects, survey_id, question_data):
    if survey_id not in survey_objects:
        survey_objects[survey_id]['questions'] = []  # Initialize questions list if not exists

    # Check if the question already exists in the list
    question_exists = any(question['id'] == question_data['question_id'] for question in survey_objects[survey_id]['questions'])

    # If the question does not exist, append it to the list
    if not question_exists:
        survey_objects[survey_id]['questions'].append({
            "id": question_data['question_id'],
            "type": question_data['question_type'],
            "question": question_data['question'],
            "options": json.loads(question_data['options']) if question_data['options'] else []
        })

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
        if not result or result[0]['MAX(response_id)'] is None:
            last_response_id = 0
        else:
            # Extract the last response ID and return it
            last_response_id = result[0]['MAX(response_id)']


        # Increment the last response_id by 1 to generate a new response_id
        new_response_id = last_response_id + 1

        # Save each question's response to the database
        for answer in data['answers']:
            survey_id = data['metadata']['survey_id']
            question_id = answer['question_id']
            answer_text = answer['answer']

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
        print(f"Error saving response to database: {e}")
        return None


# submit_response()
# Helper function to validate response data structure
def validate_response(response_data, survey_object):
    response_questions = response_data.get("answers", [])
    print(response_questions, flush=True)
    survey_questions = survey_object.get("questions", [])
    print(survey_questions, flush=True)

    # Check if the number of questions match
    if len(response_questions) != len(survey_questions):
        return "Number of questions in response does not match survey"

    # Iterate through each question in the response
    for response_question in response_questions:
        # Find the corresponding question in the survey
        matching_survey_question = next(
            (question for question in survey_questions if question["id"] == response_question["question_id"]),
            None
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
            if len(response_question.get("options", [])) != len(matching_survey_question.get("options", [])):
                return f"Number of options mismatch for question with ID {response_question['question_id']}"
            # Check if each option in the response exists in the survey question's options
            for option in response_question.get("options", []):
                if option not in matching_survey_question.get("options", []):
                    return f"Option '{option}' not found in question with ID {response_question['question_id']}'s options"

    # If all checks pass, the response object is valid
    return None

