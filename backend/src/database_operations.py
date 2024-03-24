import os
import pymysql


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
        insert_query = """
            INSERT INTO Surveys (name, description, title, subtitle, admin_username, created_at, chat_context)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """
        survey_data = (
            data['name'],
            data['description'],
            data['title'],
            data['subtitle'],
            data['admin_username'],
            data['chat_context']
        )
        execute(connection, insert_query, survey_data)

        # Get the ID of the inserted survey
        select_query = "SELECT LAST_INSERT_ID() AS survey_id"
        survey_id = fetch(connection, select_query)[0]['survey_id']

        return survey_id
    except Exception as e:
        print(f"Error creating survey: {e}")
        return None


# get_surveys()
# Helper function to create survey object
def create_survey_object(row):
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
        "questions": [],  # Initialize questions list
        "chat_context": row['chat_context']
    }
    return survey_object

