import os
import pymysql.cursors

# Connect to MySQL
mysql_host = os.getenv("MYSQL_HOST", "localhost")
mysql_user = os.getenv("MYSQL_USER", "root")
mysql_password = os.getenv("MYSQL_PASSWORD", "password")
mysql_db = os.getenv("MYSQL_DB", "ai_chat_survey_db")

connection = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_db,
    cursorclass=pymysql.cursors.DictCursor,
)


def get_connection():
    return connection


def get_cursor():
    return connection.cursor()


def close_connection():
    connection.close()


def commit():
    connection.commit()


def rollback():
    connection.rollback()


def execute(query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
    except Exception as e:
        print(f"Error executing query: {e}")
        rollback()


def fetch(query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching results: {e}")


def close_cursor(cursor):
    cursor.close()