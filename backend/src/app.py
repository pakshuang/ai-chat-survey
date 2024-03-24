import datetime
from functools import wraps
import os

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

BACKEND_CONTAINER_PORT = os.getenv("BACKEND_CONTAINER_PORT", "5000")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_key_for_development")


# Mock data


admins = {}

survey_1 = {
    "metadata": {
        "id": 1,
        "name": "name",
        "description": "description",
        "created_by": "admin",  # admin username
        "created_at": "2024-03-22 15:24:10",  # YYYY-MM-DD HH:MM:SS
    },
    "title": "title",
    "subtitle": "subtitle",
    "questions": [
        {
            "id": 1,
            "type": "multiple_choice",  # multiple_choice, short_answer, long_answer, etc.
            "question": "Which performance did you enjoy the most?",
            "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
        },
        {
            "id": 2,
            "type": "short_answer",
            "question": "What did you like about the performance?",
        },
        {
            "id": 3,
            "type": "long_answer",
            "question": "Do you have any feedback about the venue?",
        },
    ],
    "chat_context": "Full Stack Entertainment is an events company that organises performances such as concerts.",  # The proprietary knowledge that the chatbot needs to have to conduct the chat
}
survey_2 = {
    "metadata": {
        "id": 2,
        "name": "name",
        "description": "description",
        "created_by": "admin",  # admin username
        "created_at": "2024-03-22 15:25:10",  # YYYY-MM-DD HH:MM:SS
    },
    "title": "title",
    "subtitle": "subtitle",
    "questions": [
        {
            "id": 1,
            "type": "multiple_choice",  # multiple_choice, short_answer, long_answer, etc.
            "question": "Rate your experience with our service:",
            "options": ["1", "2", "3", "4", "5"],
        },
        {
            "id": 2,
            "type": "short_answer",
            "question": "Who assisted you?",
        },
        {
            "id": 3,
            "type": "long_answer",
            "question": "What can we improve?",
        },
    ],
    "chat_context": "Full Send is a retail courier company that provides mailing services for consumers. We have branches in Bishan, Changi, and Clementi.",  # The proprietary knowledge that the chatbot needs to have to conduct the chat
}

surveys = {"surveys": [survey_1, survey_2]}

responses = {"responses": []}

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

        except Exception as e:
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
    if not data or not data["username"] or not data["password"]:
        return jsonify({"message": "Missing data"}), 400

    username = data["username"]

    # TODO: Check if admin already exists
    if username in admins:
        return jsonify({"message": "Admin already exists"}), 400

    hashed_password = generate_password_hash(data["password"])

    # TODO: Save admin to database
    admins[username] = hashed_password

    return jsonify({"message": f"Admin {username} created successfully"}), 201


@app.route("/api/v1/admins/login", methods=["POST"])
def login_admin():
    data = request.get_json()

    # Basic validation
    if not data or not data["username"] or not data["password"]:
        return jsonify({"message": "Missing data"}), 400

    # TODO: Get admin's hashed password from database for authentication
    if data["username"] not in admins or not check_password_hash(
        admins[data["username"]], data["password"]
    ):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate JWT token
    token_payload = {
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24),
        "iat": datetime.datetime.now(datetime.UTC),
        "sub": data["username"],  # Admin's username
    }
    token = jwt.encode(
        token_payload, app.config["SECRET_KEY"], algorithm="HS256"
    )  # Encoded with HMAC SHA-256 algorithm
    return jsonify({"jwt": token}), 200


# Survey routes


@app.route("/api/v1/surveys", methods=["POST"])
@admin_token_required
def create_survey():
    data = request.get_json()

    # Validation
    if not data:  # TODO: Implement survey object validation
        return jsonify({"message": "Invalid data"}), 400

    # TODO: Save survey to database, record the survey ID for response
    data["metadata"]["id"] = len(surveys.surveys) + 1  # Mock
    surveys.surveys += data
    survey_id = len(surveys.surveys)  # Mock

    return jsonify({"survey_id": survey_id}), 201


@app.route("/api/v1/surveys", methods=["GET"])
def get_surveys():
    username = request.args.get("admin")
    if not username:
        return jsonify({"message": "Missing admin username"}), 400

    # TODO: Get surveys from database, filtered by admin username if specified
    filtered_surveys = list(
        filter(
            lambda survey: survey["metadata"]["created_by"] == username,
            surveys["surveys"],
        )
    )

    if not filtered_surveys:
        return jsonify({"message": "No surveys found"}), 404

    return jsonify(filtered_surveys), 200


@app.route("/api/v1/surveys/<survey_id>", methods=["GET"])
def get_survey(survey_id):
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

    # TODO: Get survey from database
    filtered_surveys = list(
        filter(
            lambda survey: survey["metadata"]["id"] == int(survey_id),
            surveys["surveys"],
        )
    )

    if not filtered_surveys:
        return jsonify({"message": "Survey not found"}), 404

    return jsonify(filtered_surveys[0]), 200


@app.route("/api/v1/surveys/<survey_id>", methods=["DELETE"])
@admin_token_required
def delete_survey(survey_id):
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

    # TODO: Check if survey exists, return 404 if not
    filtered_surveys = list(
        filter(
            lambda survey: survey["metadata"]["id"] == int(survey_id),
            surveys["surveys"],
        )
    )
    if not filtered_surveys:
        return jsonify({"message": "Survey not found"}), 404
    if filtered_surveys[0]["metadata"]["created_by"] != request["jwt_sub"]:
        return jsonify({"message": "Accessing other admin's surveys is forbidden"}), 403
    # TODO: Delete survey from database
    surveys.surveys.remove(filtered_surveys[0])

    return jsonify({"message": "Survey deleted successfully"}), 200


# Response routes


@app.route("/api/v1/responses", methods=["POST"])
def submit_response():
    data = request.get_json()
    # TODO: Validate response object against survey object, return 400 if not valid
    # TODO: Save response to database and get the response ID
    data["metadata"]["response_id"] = len(responses.responses) + 1
    response_id = len(responses.responses) + 1
    responses.responses += data

    response_body = {"response_id": response_id}

    return jsonify(response_body), 201


@app.route("/api/v1/responses", methods=["GET"])
@admin_token_required
def get_responses():
    # TODO: Check if survey ID is provided, return 400 if not
    survey_id = request.args.get("survey")
    if not survey_id:
        return jsonify({"message": "Missing survey ID"}), 400

    # TODO: Check if survey exists, return 404 if not
    filtered_surveys = list(
        filter(
            lambda survey: survey["metadata"]["id"] == int(survey_id),
            surveys["surveys"],
        )
    )
    if not filtered_surveys:
        return jsonify({"message": "Survey not found"}), 404

    # TODO: Check if admin has access to survey, return 403 if not
    survey = filtered_surveys[0]
    if survey["metadata"]["created_by"] != request["jwt_sub"]:
        return jsonify({"message": "Accessing other admin's surveys is forbidden"}), 403

    # TODO: Get responses from database
    responses = list(
        filter(
            lambda response: response["metadata"]["survey_id"] == int(survey_id),
            responses["responses"],
        )
    )
    return jsonify(responses), 200


@app.route("/api/v1/responses/<response_id>", methods=["GET"])
@admin_token_required
def get_response(response_id):
    # TODO: Check if response exists, return 404 if not
    responses = list(
        filter(
            lambda response: response["metadata"]["response_id"] == int(response_id),
            responses["responses"],
        )
    )
    if not responses:
        return jsonify({"message": "Response not found"}), 404
    response = responses[0]

    # TODO: Check if corresponding survey exists, return 404 if not
    filtered_surveys = list(
        filter(
            lambda survey: survey["metadata"]["id"]
            == int(response["metadata"]["survey_id"]),
            surveys["surveys"],
        )
    )
    if not filtered_surveys:
        return jsonify({"message": "Survey not found"}), 404
    survey = filtered_surveys[0]

    # TODO: Check if admin has access to survey, return 403 if not
    if survey["metadata"]["created_by"] != request["jwt_sub"]:
        return jsonify({"message": "Accessing other admin's surveys is forbidden"}), 403

    return jsonify(response), 200


@app.route("/api/v1/responses/<response_id>/chat", methods=["POST"])
def send_chat_message(response_id):
    # TODO: Check if response exists, return 404 if not
    responses = list(
        filter(
            lambda response: response["metadata"]["response_id"] == int(response_id),
            responses["responses"],
        )
    )
    if not responses:
        return jsonify({"message": "Response not found"}), 404

    data = request.get_json()
    if not data or data["content"] is None:
        return jsonify({"message": "Missing data"}), 400

    # TODO: Save message to database
    # TODO: Get reply from LLM
    # TODO: Save reply to database

    import random

    is_last = random.randint(0, 1) < 0.1
    return (
        jsonify(
            {"content": "This is a dummy reply from the chatbot.", "is_last": is_last}
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=BACKEND_CONTAINER_PORT)
