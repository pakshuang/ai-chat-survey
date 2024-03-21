import datetime
from functools import wraps
import os

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

BACKEND_CONTAINER_PORT = os.getenv("BACKEND_CONTAINER_PORT", "5000")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_key_for_development')


# JWT


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is in the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        # If no token found, return error
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # Pass some payload information to the route function
        kwargs['jwt_sub'] = payload['sub']

        return f(*args, **kwargs)

    return decorated


# Admin routes


@app.route('/api/v1/admins', methods=['POST'])
def create_admin():
    data = request.get_json()

    # Basic validation
    if not data or not data['username'] or not data['password']:
        return jsonify({'message': 'Missing data'}), 400

    # Check if admin already exists
    if False:  #TODO: Check if admin already exists
        return jsonify({'message': 'Admin already exists'}), 400

    username = data['username']
    hashed_password = generate_password_hash(data['password'], method='bcrypt')

    # TODO: Save admin to database

    return jsonify({'message': f'Admin {username} created successfully'}), 201


@app.route('/api/v1/admins/login', methods=['POST'])
def login_admin():
    data = request.get_json()

    # Basic validation
    if not data or not data['username'] or not data['password']:
        return jsonify({'message': 'Missing data'}), 400

    admin = {"username": data['username'], "password": "hashed_password"}  #TODO: Actually get admin from database where username=data['username']

    if admin: # and check_password_hash(admin.password, data['password']):
        token_payload = {
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24),
            'iat': datetime.datetime.now(datetime.UTC),
            'sub': admin.username,  # Admin's username
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256') # Encoded with HMAC SHA-256 algorithm
        return jsonify({'jwt': token.decode('UTF-8')}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


# Survey routes


@app.route('/api/v1/surveys', methods=['POST'])
@admin_token_required
def create_survey():
    data = request.get_json()

    # Validation
    if not data: # TODO: Implement survey object validation
        return jsonify({'message': 'Invalid data'}), 400
    
    # TODO: Save survey to database, record the survey ID for response
    survey_id = 1 # Mock

    return jsonify({'survey_id': survey_id}), 201


@app.route('/api/v1/surveys', methods=['GET'])
@admin_token_required
def get_surveys():
    admin = request.args.get('admin')

    # TODO: Get surveys from database, filtered by admin username if specified
    surveys = {"surveys": []}

    return jsonify(surveys), 200


@app.route('/api/v1/surveys/<survey_id>', methods=['GET'])
def get_survey(survey_id):
    # TODO: Get survey from database, return 404 if not found
    
    survey = {}
    return jsonify(survey), 200


@app.route('/api/v1/surveys/<survey_id>', methods = ['DELETE'])
@admin_token_required
def delete_survey(survey_id):
    if not survey_id:
        return jsonify({'message': 'Missing survey ID'}), 400
    # TODO: Check if survey exists, return 404 if not
    survey = {"metadata": {"created_by": "username"}} # TODO: Actually get survey from database
    if survey.metadata.created_by != request.jwt_sub:
        return jsonify({'message': "Accessing other admin's surveys is forbidden"}), 403
    # TODO: Delete survey from database

    return jsonify({'message': 'Survey deleted successfully'}), 200


# Response routes


@app.route('/api/v1/surveys/<survey_id>/responses', methods=['POST'])
def submit_response(survey_id):
    # TODO: Check if survey exists, return 404 if not
    # TODO: Get survey
        
    data = request.get_json()
    # TODO: Validate response object against survey object, return 400 if not valid
    # TODO: Save response to database and get the response ID
    response_id = 1 # Mock

    response_body = {"response_id": "string"}

    return jsonify(response_body), 201


@app.route('/api/v1/surveys/<survey_id>/responses', methods=['GET'])
@admin_token_required
def get_responses(survey_id):
    # TODO: Check if survey exists, return 404 if not
    survey = {"metadata": {"created_by": "username"}} # TODO: Actually get survey from database
    if survey.metadata.created_by != request.jwt_sub:
        return jsonify({'message': "Accessing other admin's surveys is forbidden"}), 403
    # TODO: Get responses from database
    responses = {"responses": []}
    return jsonify(responses), 200


@app.route('/api/v1/surveys/<survey_id>/responses/<response_id>', methods=['GET'])
@admin_token_required
def get_response(survey_id, response_id):
    # TODO: Check if survey exists, return 404 if not
    survey = {"metadata": {"created_by": "username"}} # TODO: Actually get survey from database
    if survey.metadata.created_by != request.jwt_sub:
        return jsonify({'message': "Accessing other admin's surveys is forbidden"}), 403
    # TODO: Check if response exists, return 404 if not
    # TODO: Get response from database
    response = {}
    return jsonify(response), 200


@app.route('/api/v1/surveys/<survey_id>/responses/<response_id>/chat', methods=['POST'])
def send_chat_message(survey_id, response_id):
    # TODO: Check if survey exists, return 404 if not
    # TODO: Check if response exists, return 404 if not
    data = request.get_json()
    if not data or data['content'] is None:
        return jsonify({'message': 'Missing data'}), 400
    # TODO: Save message to database
    # TODO: Get reply from LLM
    # TODO: Save reply to database
    return jsonify({'message': 'Message sent successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=BACKEND_CONTAINER_PORT)