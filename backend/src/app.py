# -*- coding: utf-8 -*-
"""
    src.app
    ~~~~~~~

    This module implements the API for the backend server.
"""


import datetime
import json
import logging
import os
from functools import wraps

import jwt
from flask import Flask, Response, jsonify, request
from src import database_operations
from src.llm_classes.chatlog import ChatLog
from src.llm_classes.functions import (
    check_exit,
    construct_chatlog,
    format_responses_for_gpt,
)
from src.llm_classes.llm_level import GPT
from werkzeug.security import check_password_hash, generate_password_hash

BACKEND_CONTAINER_PORT = os.getenv("BACKEND_CONTAINER_PORT", "5000")

logging.basicConfig(
    filename="./logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "default_key_for_development"
)

# JWT


def admin_token_required(f: callable) -> callable:
    """Decorator function to check if a valid JWT token is provided in the request headers

    Args:
        f (callable): Function to be decorated

    Returns:
        callable: Decorated function
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        # If no token found, return error
        if not token:
            app.logger.info("Token is missing!")
            return jsonify({"message": "Token is missing!"}), 400

        try:
            # Decode the token
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            app.logger.info("Token is valid")

        except jwt.InvalidTokenError:
            app.logger.info("Token is invalid! Token: " + str(token))
            return jsonify({"message": "Token is invalid!"}), 401

        # Pass some payload information to the route function
        kwargs["jwt_sub"] = payload["sub"]

        return f(*args, **kwargs)

    return decorated


# Health check route


@app.route("/api/v1/health", methods=["GET"])
def health_check() -> tuple[Response, int]:
    """Health check route

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    return jsonify({"message": "Server is running!"}), 200


# Admin routes


@app.route("/api/v1/admins", methods=["POST"])
def create_admin() -> tuple[Response, int]:
    """Create an admin account

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    data = request.get_json()

    # Basic validation
    if not data or not data.get("username") or not data.get("password"):
        app.logger.info("Missing data")
        return jsonify({"message": "Missing data"}), 400

    username = data["username"]
    connection = database_operations.connect_to_mysql()
    if connection:
        query = "SELECT * FROM Admins WHERE admin_username = %s"
        existing_admins = database_operations.fetch(connection, query, (username,))

        # If admin exists
        if existing_admins:
            database_operations.close_connection(connection)
            return jsonify({"message": "Admin already exists"}), 400

        # Hash password for storage
        hashed_password = generate_password_hash(
            data["password"], method="pbkdf2:sha256", salt_length=8
        )

        # Save admin to database
        query = "INSERT INTO Admins (admin_username, password, created_at) VALUES (%s, %s, NOW())"
        params = (username, hashed_password)
        database_operations.execute(connection, query, params)

        database_operations.close_connection(connection)
        app.logger.info(f"Admin {username} created successfully")
        return jsonify({"message": f"Admin {username} created successfully"}), 201
    else:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to the database"}), 500


@app.route("/api/v1/admins/login", methods=["POST"])
def login_admin() -> tuple[Response, int]:
    """Login an admin

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    data = request.get_json()

    # Basic validation
    if not data or not data.get("username") or not data.get("password"):
        app.logger.info("Missing data")
        return jsonify({"message": "Missing data"}), 400

    # Retrieve hashed password from database
    # Connect to database
    connection = database_operations.connect_to_mysql()
    if connection:
        # Retrieve admin_usernames
        query = "SELECT password FROM Admins WHERE admin_username = %s"
        result = database_operations.fetch(connection, query, (data["username"],))
        if result:
            hashed_password = result[0]["password"]
            # Check if the provided password matches the hashed password
            if check_password_hash(hashed_password, data["password"]):
                # Generate the jwt_token
                token_payload = {
                    "exp": datetime.datetime.now(datetime.UTC)
                    + datetime.timedelta(hours=24),
                    "iat": datetime.datetime.now(datetime.UTC),
                    "sub": data["username"],  # Admin's username
                }
                token = jwt.encode(
                    token_payload, app.config["SECRET_KEY"], algorithm="HS256"
                )  # Encoded with HMAC SHA-256 algorithm

                # Close the connection
                database_operations.close_connection(connection)
                app.logger.info(f"Admin {data['username']} logged in successfully")
                return (
                    jsonify(
                        {
                            "jwt": token,
                            "jwt_exp": token_payload["exp"].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    ),
                    200,
                )
        # Close the connection
        database_operations.close_connection(connection)
        app.logger.info("Invalid credentials")
        return jsonify({"message": "Invalid credentials"}), 401
    else:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to the database"}), 500


# Survey routes


@app.route("/api/v1/surveys", methods=["POST"])
@admin_token_required
def create_survey(**kwargs) -> tuple[Response, int]:
    """Create a survey

    Args:
        kwargs (dict): Dictionary containing the JWT token subject claim (jwt_sub: admin username)

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    data = request.get_json()

    # If there is no data attached in request body
    if not data:
        app.logger.info("No survey object was attached")
        return jsonify({"message": "Missing data"}), 400
    # Validate survey object format
    is_valid, message = database_operations.validate_survey_object(data)
    if not is_valid:
        app.logger.info(f"Invalid survey object format: {message}")
        return jsonify({"message": message}), 400

    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Error connecting to database"}), 500

    try:
        # Create the survey
        survey_id = database_operations.create_survey(connection, data)

        if survey_id:
            app.logger.info(f"Survey {survey_id} created successfully")
            return jsonify({"survey_id": survey_id}), 201
        else:
            app.logger.error("Error creating survey")
            return jsonify({"message": "Error creating survey"}), 400
    except Exception as e:
        app.logger.error(f"Error creating survey: {str(e)}")
        return jsonify({"message": "Error creating survey"}), 400
    finally:
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys", methods=["GET"])
def get_surveys() -> tuple[Response, int]:
    """Get all surveys

    Query Parameters:
        admin (str, optional): Admin username to filter surveys by

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to database"}), 500

    try:
        # Check for optional username argument
        username = request.args.get("admin", None)

        if username:
            query = """
                    SELECT Surveys.*, Questions.* 
                    FROM Surveys 
                    LEFT JOIN Questions ON Surveys.survey_id = Questions.survey_id 
                    WHERE Surveys.admin_username = %s 
                    ORDER BY Surveys.survey_id DESC, Questions.question_id  
            """
            params = (username,)
        else:
            query = """
            SELECT Surveys.*, Questions.* 
            FROM Surveys 
            LEFT JOIN Questions ON Surveys.survey_id = Questions.survey_id 
            ORDER BY Surveys.survey_id DESC, Questions.question_id
            """
            params = None

        survey_data = database_operations.fetch(connection, query, params)

        if survey_data is None:
            app.logger.error("Error fetching surveys: Database error")
            return jsonify({"message": "Error fetching surveys"}), 500
        elif not survey_data:
            app.logger.info("No surveys found")
            return jsonify([]), 200

        # Group survey data by survey ID and collect questions
        survey_objects = {}
        for row in survey_data:
            survey_id = row["survey_id"]
            if survey_id not in survey_objects:
                survey_objects[survey_id] = database_operations.create_survey_object(
                    row
                )
            if row["question_id"] is not None:  # Check if there's a question associated
                database_operations.append_question_to_survey(
                    survey_objects, survey_id, row
                )

        # Convert dictionary to list of survey objects
        survey_objects_list = list(survey_objects.values())

        app.logger.info("Surveys fetched successfully")
        return jsonify(survey_objects_list), 200
    except Exception as e:
        app.logger.error("Error fetching surveys: Database error")
        return jsonify({"message": "Error fetching surveys"}), 500
    finally:
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys/<survey_id>", methods=["GET"])
def get_survey(survey_id: str) -> tuple[Response, int]:
    """Get a survey by ID

    Args:
        survey_id (str): Survey ID

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    if not survey_id:
        app.logger.info("Missing survey ID")
        return jsonify({"message": "Missing survey ID"}), 400

    # Get survey from database
    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to database"}), 500

    try:
        query = """
            SELECT Surveys.*, Questions.* 
            FROM Surveys 
            LEFT JOIN Questions ON Surveys.survey_id = Questions.survey_id 
            WHERE Surveys.survey_id = %s
            ORDER BY Surveys.survey_id DESC, Questions.question_id
        """
        params = (survey_id,)

        survey_data = database_operations.fetch(connection, query, params)
        if survey_data is None:
            app.logger.error("Error fetching survey: Database error")
            return jsonify({"message": "Error fetching survey"}), 500
        elif not survey_data:
            app.logger.info("Survey not found")
            return jsonify({"message": "Survey not found"}), 404

        # Group survey data by survey ID and collect questions
        survey_object = {}
        for row in survey_data:
            survey_id = row["survey_id"]
            if survey_id not in survey_object:
                survey_object[survey_id] = database_operations.create_survey_object(row)
            if row["question_id"] is not None:  # Check if there's a question associated
                database_operations.append_question_to_survey(
                    survey_object, survey_id, row
                )
        survey_object = survey_object[int(survey_id)]
        app.logger.info("Survey fetched successfully")
        return jsonify(survey_object), 200
    except Exception as e:
        app.logger.error(f"Error fetching survey: {str(e)}")
        return jsonify({"message": "Error fetching surveys"}), 500
    finally:
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys/<survey_id>", methods=["DELETE"])
@admin_token_required
def delete_survey(survey_id: str, **kwargs) -> tuple[Response, int]:
    """Delete a survey by ID

    Args:
        survey_id (str): Survey ID
        kwargs (dict): Dictionary containing the JWT token subject claim (jwt_sub: admin username)

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    # Check if survey exists, return 404 if not
    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to the database"}), 500

    try:
        # Check if the survey exists
        survey_query = "SELECT * FROM Surveys WHERE survey_id = %s"
        survey = database_operations.fetch(connection, survey_query, (survey_id,))
        if not survey:
            app.logger.info("Survey not found")
            return jsonify({"message": "Survey not found"}), 404

        # Check if the user has permission to delete the survey
        if survey[0]["admin_username"] != kwargs["jwt_sub"]:
            return (
                jsonify({"message": "Accessing other admin's surveys is forbidden"}),
                403,
            )

        # Delete the survey
        delete_survey_query = "DELETE FROM Surveys WHERE survey_id = %s"
        database_operations.execute(connection, delete_survey_query, (survey_id,))
        database_operations.commit(connection)

        app.logger.info("Survey deleted successfully")
        return jsonify({"message": "Survey deleted successfully"}), 200

    except Exception as e:
        app.logger.error(f"Failed to delete survey: {str(e)}")
        return jsonify({"message": "Failed to delete survey"}), 500

    finally:
        database_operations.close_connection(connection)


# Response routes


@app.route("/api/v1/surveys/<survey_id>/responses", methods=["POST"])
def submit_response(survey_id: str) -> tuple[Response, int]:
    """Submit a response to a survey

    Args:
        survey_id (str): Survey ID

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    data = request.get_json()
    if not data:
        app.logger.info("No data was attached")
        return jsonify({"message": "No data was attached"}), 400

    # Validate response object format
    is_valid, message = database_operations.validate_response_object(data)
    if not is_valid:
        app.logger.info(f"Invalid response object format: {message}")
        return jsonify({"message": message}), 400

    # Retrieve survey object from the database
    survey_object_response = get_survey(survey_id)

    # If GET request is not successful, return 500
    if survey_object_response[1] != 200:
        app.logger.error("Failed to retrieve survey object")
        return jsonify({"message": "Failed to retrieve survey object"}), 500

    # GET request is successful
    survey_object = survey_object_response[0].json

    # Validate response object against survey object
    validation_error = database_operations.validate_response(data, survey_object)
    if validation_error:
        app.logger.info(f"Validation error: {validation_error}")
        return jsonify({"message": validation_error}), 400

    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if connection is None:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to the database"}), 500

    # Insert data into database
    try:
        # Save response to database and get the response ID
        response_id = database_operations.save_response_to_database(
            connection, data, str(survey_id)
        )

        if response_id is None:
            app.logger.error("Failed to save response to the database")
            return jsonify({"message": "Failed to save response to the database"}), 500

        response_body = {"response_id": response_id}

        app.logger.info("Response submitted successfully")
        return jsonify(response_body), 201
    finally:
        # Close database connection
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys/<survey_id>/responses", methods=["GET"])
@admin_token_required
def get_responses(survey_id: str, **kwargs) -> tuple[Response, int]:
    """Get all responses to a survey

    Args:
        survey_id (str): Survey ID
        kwargs (dict): Dictionary containing the JWT token subject claim (jwt_sub: admin username)

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """

    # Connect to MySQL database
    connection = database_operations.connect_to_mysql()
    if not connection:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to the database"}), 500
    try:
        # Fetch survey from the database
        query = """
            SELECT * FROM Surveys WHERE survey_id = %s
        """
        survey = database_operations.fetch(connection, query, (survey_id,))

        # Check if survey exists
        if not survey:
            app.logger.info("Survey not found")
            return jsonify({"message": "Survey not found"}), 404

        # Check if admin has access to survey, return 403 if not
        if survey[0]["admin_username"] != kwargs["jwt_sub"]:
            return (
                jsonify({"message": "Accessing other admin's surveys is forbidden"}),
                403,
            )

        # Fetch responses from the database
        query = """
            SELECT sr.response_id, sr.submitted_at, sr.question_id, q.question_type, q.question, q.options, sr.answer
            FROM Survey_Responses sr
            INNER JOIN Questions q ON sr.question_id = q.question_id AND sr.survey_id = q.survey_id
            INNER JOIN Surveys s ON sr.survey_id = s.survey_id
            WHERE sr.survey_id = %s
        """
        responses_data = database_operations.fetch(connection, query, (survey_id,))

        # Check if responses exist
        if not responses_data:
            app.logger.info("No responses found for the survey")
            return jsonify([]), 200

        # Create response objects dictionary
        response_objects = {}
        for response_data in responses_data:
            response_id = response_data["response_id"]
            if response_id not in response_objects:
                response_objects[response_id] = (
                    database_operations.create_response_object(
                        survey_id, response_id, response_data
                    )
                )
            # Retrieve chatlog if it exists
            chat_log_query = """
            SELECT chat_log FROM ChatLog WHERE survey_id = %s AND response_id = %s
            """
            chat_log_data = database_operations.fetch(
                connection, chat_log_query, (survey_id, response_id)
            )
            database_operations.append_answer_to_response(
                response_objects,
                response_id,
                response_data,
                chat_log_data,
            )

        # Convert dictionary to list of response objects
        response_objects_list = list(response_objects.values())

        app.logger.info("Responses fetched successfully")
        return jsonify(response_objects_list), 200
    finally:
        # Close database connection
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys/<survey_id>/responses/<response_id>", methods=["GET"])
@admin_token_required
def get_response(survey_id: str, response_id: str, **kwargs) -> tuple[Response, int]:
    """Get a response by response ID and survey ID

    Args:
        survey (str): Survey ID
        response_id (str): Response ID

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """

    # Connect to MySQL database
    connection = database_operations.connect_to_mysql()
    if not connection:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to the database"}), 500

    try:
        # Fetch survey from the database
        query = """
            SELECT * FROM Surveys WHERE survey_id = %s
        """
        survey = database_operations.fetch(connection, query, (survey_id,))

        # Check if survey exists
        if not survey:
            app.logger.info("Survey not found")
            return jsonify({"message": "Survey not found"}), 404

        # Check if admin has access to survey
        if survey[0]["admin_username"] != kwargs["jwt_sub"]:
            app.logger.info("Accessing other admin's surveys is forbidden")
            return (
                jsonify({"message": "Accessing other admin's surveys is forbidden"}),
                403,
            )

        # Fetch responses from the database
        query = """
            SELECT sr.response_id, sr.submitted_at, sr.question_id, q.question_type, q.question, q.options, sr.answer
            FROM Survey_Responses sr
            INNER JOIN Questions q ON sr.question_id = q.question_id AND sr.survey_id = q.survey_id
            INNER JOIN Surveys s ON sr.survey_id = s.survey_id
            WHERE sr.survey_id = %s AND sr.response_id = %s
        """
        responses_data = database_operations.fetch(
            connection, query, (survey_id, response_id)
        )

        # Check if responses exist
        if not responses_data:
            app.logger.info("No responses found for the survey")
            return jsonify([]), 200

        # Create response objects dictionary
        response_objects = {}
        for response_data in responses_data:
            response_id = response_data["response_id"]
            if response_id not in response_objects:
                response_objects[response_id] = (
                    database_operations.create_response_object(
                        survey_id, response_id, response_data
                    )
                )
            # Retrieve chatlog if it exists
            chat_log_query = """
            SELECT chat_log FROM ChatLog WHERE survey_id = %s AND response_id = %s
            """
            chat_log_data = database_operations.fetch(
                connection, chat_log_query, (survey_id, response_id)
            )
            database_operations.append_answer_to_response(
                response_objects,
                response_id,
                response_data,
                chat_log_data,
            )
        response_objects = response_objects[int(response_id)]
        app.logger.info("Response fetched successfully")
        return jsonify(response_objects), 200
    finally:
        # Close database connection
        database_operations.close_connection(connection)


def helper_send_message(
    llm_input: dict[str, object], user_input: str, connection, survey_id, response_id
) -> tuple[Response, int]:
    """Generates a response from a large language model.

    Args:
        llm_input (dict): A dictionary dict[str, object]  which contains a chat context string,
        response object, and message list
        user_input (str): User input
        connection: MySQL connection object
        survey_id (str): Survey ID
        response_id (str): Response ID

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """

    def has_no_chat_log(content: str, message_list: list[dict[str, object]]) -> bool:
        return not content.strip() and not message_list

    try:
        # initialise LLM
        llm = GPT()
        chat_log_dict = json.loads(llm_input["chat_log"])
        message_list = chat_log_dict["messages"]

        has_no_chat_log = has_no_chat_log(user_input, message_list)
        if has_no_chat_log:
            pipe = construct_chatlog(
                f"""{llm_input["chat_context"]}\n{
                    format_responses_for_gpt(
                        llm_input["response_object"]
                    )
                }""",
                llm=llm,
            )
            first_question = llm.run(pipe.message_list, with_moderation=False)
            updated_message_list = pipe.insert_and_update(
                first_question, pipe.current_index, is_llm=True
            )

        else:
            pipe = ChatLog(message_list, llm=llm)
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
            database_operations.update_chat_log(
                connection, survey_id, response_id, updated_chat_log_json
            )
        except Exception as e:
            app.logger.error(
                "An error occurred while updating chat log with user message: " + str(e)
            )
            return (
                jsonify({"message": "An error occurred while updating the chat log"}),
                500,
            )

        content = updated_message_list[-1]["content"]

        is_last = check_exit(updated_message_list, llm)
        database_operations.close_connection(connection)
        app.logger.info("Reply generated successfully")
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
        app.logger.error("An error was encountered while generating a reply: " + str(e))
        return (
            jsonify(
                {
                    "message": "An error was encountered while generating a reply: "
                    + str(e)
                }
            ),
            500,
        )


@app.route("/api/v1/surveys/<survey_id>/responses/<response_id>/chat", methods=["POST"])
def send_chat_message(survey_id: str, response_id: str) -> tuple[Response, int]:
    """Send a chat message for a response

    Args:
        survey (str): Survey ID
        response_id (str): Response ID

    Returns:
        tuple[Response, int]: Tuple containing the response and status code
    """
    # Check that there is "content" in request body
    data = request.get_json()
    if "content" not in data:
        app.logger.info("Missing content")
        return jsonify({"message": "Missing content"}), 400

    # Step 1: Retrieve Response Object
    response_object = get_response_no_auth(survey_id, response_id)

    # If GET request is not successful
    if response_object[1] != 200:
        app.logger.error(response_object[0].json.get("message"))
        return response_object

    # GET request is successful
    response_object = response_object[0].json

    # Connect to MySQL database
    connection = database_operations.connect_to_mysql()
    if not connection:
        app.logger.error("Failed to connect to the database")
        return jsonify({"message": "Failed to connect to the database"}), 500

    # Step 2: Insert message to DB
    try:
        chat_log = database_operations.get_chat_log(connection, survey_id, response_id)
        chat_log_dict = json.loads(chat_log)

        if data["content"]:
            # Append new message to the messages list
            chat_log_dict["messages"].append(
                {"role": "user", "content": data["content"]}
            )

            # Convert the updated chat log dictionary back to a JSON string
            updated_chat_log = json.dumps(chat_log_dict)
            database_operations.update_chat_log(
                connection, survey_id, response_id, updated_chat_log
            )
    except Exception as e:
        app.logger.error(
            "An error occurred while updating chat log with user message: " + str(e)
        )
        return (
            jsonify(
                {
                    "message": "An error occurred while updating chat log with user message"
                }
            ),
            500,
        )

    # Step 3: Retrieve chat_context
    try:
        chat_context = database_operations.fetch_chat_context(connection, survey_id)
    except Exception as e:
        app.logger.error("An error occurred while fetching chat context: " + str(e))
        return (
            jsonify({"message": "An error occurred while fetching chat context"}),
            500,
        )

    # Step 4: Retrieve chatLog object
    try:
        chat_log = database_operations.get_chat_log(connection, survey_id, response_id)
    except Exception as e:
        app.logger.error("An error occurred while fetching chat log: " + str(e))
        return jsonify({"message": "An error occurred while fetching chat log"}), 500

    # Create the object to parse into ChatGPT
    llm_input = {
        "chat_context": chat_context,
        "response_object": response_object,
        "chat_log": chat_log,
    }

    return helper_send_message(
        llm_input, data["content"], connection, survey_id, response_id
    )


# TODO: Think of a better way than having the same function without authentication
# Function to get response object without admin token required
# Exactly the same as get_response except it is not an endpoint, and there is no admin verification token.
def get_response_no_auth(survey_id, response_id):
    # Connect to MySQL database
    connection = database_operations.connect_to_mysql()
    if not connection:
        return jsonify({"message": "Failed to connect to the database"}), 500

    try:
        # Fetch survey from the database
        query = """
            SELECT * FROM Surveys WHERE survey_id = %s
        """
        survey = database_operations.fetch(connection, query, (survey_id,))

        # Check if survey exists
        if not survey:
            return jsonify({"message": "Survey not found"}), 404

        # Fetch responses from the database
        query = """
            SELECT sr.response_id, sr.submitted_at, sr.question_id, q.question_type, q.question, q.options, sr.answer
            FROM Survey_Responses sr
            INNER JOIN Questions q ON sr.question_id = q.question_id AND sr.survey_id = q.survey_id
            INNER JOIN Surveys s ON sr.survey_id = s.survey_id
            WHERE sr.survey_id = %s AND sr.response_id = %s
        """
        responses_data = database_operations.fetch(
            connection, query, (survey_id, response_id)
        )

        # Check if responses exist
        if not responses_data:
            app.logger.info("No responses found for the survey")
            return jsonify([]), 200

        # Create response objects dictionary
        response_objects = {}
        for response_data in responses_data:
            response_id = response_data["response_id"]
            if response_id not in response_objects:
                response_objects[response_id] = (
                    database_operations.create_response_object(
                        survey_id, response_id, response_data
                    )
                )
            database_operations.append_answer_to_response(
                response_objects,
                response_id,
                response_data,
                [],
            )
        response_objects = response_objects[int(response_id)]
        return jsonify(response_objects), 200
    finally:
        # Close database connection
        database_operations.close_connection(connection)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=BACKEND_CONTAINER_PORT)
