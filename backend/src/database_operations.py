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
