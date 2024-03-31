import datetime
import json
import os
from functools import wraps

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS
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

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "default_key_for_development"
)


@app.after_request
def handle_options(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return response


# JWT


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        # If no token found, return error
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode the token
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])

        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401

        # Pass some payload information to the route function
        kwargs["jwt_sub"] = payload["sub"]

        return f(*args, **kwargs)

    return decorated


# Health check route


@app.route("/api/v1/health", methods=["GET"])
def health_check():
    return jsonify({"message": "Server is running!"}), 200


# Admin routes


@app.route("/api/v1/admins", methods=["POST"])
def create_admin():
    data = request.get_json()

    # Basic validation
    if not data or not data.get("username") or not data.get("password"):
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
        return jsonify({"message": f"Admin {username} created successfully"}), 201
    else:
        return jsonify({"message": "Failed to connect to the database"}), 500


@app.route("/api/v1/admins/login", methods=["POST"])
def login_admin():
    data = request.get_json()

    # Basic validation
    if not data or not data.get("username") or not data.get("password"):
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
        return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "Failed to connect to the database"}), 500


# Survey routes


@app.route("/api/v1/surveys", methods=["POST"])
@admin_token_required
def create_survey(**kwargs):
    data = request.get_json()

    # If there is no data attached in request body
    if not data:
        return jsonify({"message": "Invalid data"}), 400
    # Validate survey object format
    is_valid, message = database_operations.validate_survey_object(data)
    if not is_valid:
        return jsonify({"message": message}), 400

    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
        return jsonify({"message": "Error connecting to database"}), 500

    try:
        # Create the survey
        survey_id = database_operations.create_survey(connection, data)

        if survey_id:
            return jsonify({"survey_id": survey_id}), 201
        else:
            return jsonify({"message": "Error creating survey"}), 400
    except Exception as e:
        return jsonify({"message": "Error creating survey"}), 400
    finally:
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys", methods=["GET"])
def get_surveys():
    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
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
            return jsonify({"message": "Error fetching surveys"}), 500
        elif not survey_data:
            if username:
                return jsonify([]), 200
            else:
                return jsonify({"message": "No surveys found"}), 404

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

        return jsonify(survey_objects_list), 200
    except Exception as e:
        return jsonify({"message": "Error fetching surveys"}), 500
    finally:
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys/<survey_id>", methods=["GET"])
def get_survey(survey_id):
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

    # Get survey from database
    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
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
            return jsonify({"message": "Error fetching survey"}), 500
        elif not survey_data:
            return jsonify({"message": "No survey found"}), 404

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
        return jsonify(survey_object), 200
    except Exception as e:
        return jsonify({"message": "Error fetching surveys"}), 500
    finally:
        database_operations.close_connection(connection)


@app.route("/api/v1/surveys/<survey_id>", methods=["DELETE"])
@admin_token_required
def delete_survey(survey_id, **kwargs):
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

    # Check if survey exists, return 404 if not
    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if not connection:
        return jsonify({"message": "Failed to connect to the database"}), 500

    try:
        # Check if the survey exists
        survey_query = "SELECT * FROM Surveys WHERE survey_id = %s"
        survey = database_operations.fetch(connection, survey_query, (survey_id,))
        if not survey:
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

        return jsonify({"message": "Survey deleted successfully"}), 200

    except Exception as e:
        return jsonify({"message": "Failed to delete survey"}), 500

    finally:
        database_operations.close_connection(connection)


# Response routes


@app.route("/api/v1/responses", methods=["POST"])
def submit_response():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data was attached"}), 400

    # Validate survey object format
    is_valid, message = database_operations.validate_response_object(data)
    if not is_valid:
        return jsonify({"message": message}), 400

    # Validate response object against survey object
    # Retrieve survey object from the database
    survey_id = data["metadata"]["survey_id"]
    survey_object_response = get_survey(survey_id)

    # If GET request is not successful, return 500
    if survey_object_response[1] != 200:
        return jsonify({"message": "Failed to retrieve survey object"}), 500

    # GET request is successful
    survey_object = survey_object_response[0].json

    # Validate response object against survey object
    validation_error = database_operations.validate_response(data, survey_object)
    if validation_error:
        return jsonify({"message": validation_error}), 400

    # Connect to the database
    connection = database_operations.connect_to_mysql()
    if connection is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    # Insert data into database
    try:
        # Save response to database and get the response ID
        response_id = database_operations.save_response_to_database(
            connection, data, str(survey_id)
        )

        if response_id is None:
            return jsonify({"message": "Failed to save response to the database"}), 500

        response_body = {"response_id": response_id}

        return jsonify(response_body), 201
    finally:
        # Close database connection
        database_operations.close_connection(connection)


@app.route("/api/v1/responses", methods=["GET"])
@admin_token_required
def get_responses(**kwargs):
    # Check if survey ID is provided, return 400 if not
    survey_id = request.args.get("survey")
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

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
            return jsonify({"message": "No responses found for the survey"}), 404

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
                response_objects, response_id, response_data
            )

        # Convert dictionary to list of response objects
        response_objects_list = list(response_objects.values())

        return jsonify(response_objects_list), 200
    finally:
        # Close database connection
        database_operations.close_connection(connection)


@app.route("/api/v1/responses/<response_id>", methods=["GET"])
@admin_token_required
def get_response(response_id, **kwargs):
    if not response_id:
        return jsonify({"message": "Missing response ID"}), 400

    # Check if survey ID is provided, return 400 if not
    survey_id = request.args.get("survey")
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

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

        # Check if admin has access to survey
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
            WHERE sr.survey_id = %s AND sr.response_id = %s
        """
        responses_data = database_operations.fetch(
            connection, query, (survey_id, response_id)
        )

        # Check if responses exist
        if not responses_data:
            return jsonify({"message": "No responses found for the survey"}), 404

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
                response_objects, response_id, response_data
            )
        response_objects = response_objects[int(response_id)]
        return jsonify(response_objects), 200
    finally:
        # Close database connection
        database_operations.close_connection(connection)


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
            database_operations.update_chat_log(
                connection, survey_id, response_id, updated_chat_log_json
            )
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
        database_operations.close_connection(connection)
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


@app.route("/api/v1/responses/<response_id>/chat", methods=["POST"])
def send_chat_message(response_id):
    # Check that there is "content" in request body
    data = request.get_json()
    if "content" not in data:
        return jsonify({"message": "Missing content"}), 400

    if not response_id:
        return jsonify({"message": "Missing response ID"}), 400

    # Check if survey ID is provided, return 400 if not
    survey_id = request.args.get("survey")
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

    # Step 1: Retrieve Response Object
    response_object = get_response_no_auth(response_id=response_id, survey_id=survey_id)

    # If GET request is not successful, return 500
    if response_object[1] != 200:
        return jsonify({"message": "Failed to retrieve survey object"}), 500

    # GET request is successful
    response_object = response_object[0].json

    # Connect to MySQL database
    connection = database_operations.connect_to_mysql()
    if not connection:
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
        return (
            jsonify({"message": "An error occurred while fetching chat context"}),
            500,
        )

    # Step 4: Retrieve chatLog object
    try:
        chat_log = database_operations.get_chat_log(connection, survey_id, response_id)
    except Exception as e:
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
def get_response_no_auth(response_id, **kwargs):
    if not response_id:
        return jsonify({"message": "Missing response ID"}), 400

    # Check if survey ID is provided, return 400 if not
    survey_id = request.args.get("survey")
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

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
            return jsonify({"message": "No responses found for the survey"}), 404

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
                response_objects, response_id, response_data
            )
        response_objects = response_objects[int(response_id)]
        return jsonify(response_objects), 200
    finally:
        # Close database connection
        database_operations.close_connection(connection)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=BACKEND_CONTAINER_PORT)
