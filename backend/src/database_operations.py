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
            "options": [] if question_data['options'] is None else question_data['options'].split(',')
        })

