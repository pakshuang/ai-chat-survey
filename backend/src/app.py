import datetime
import os

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

BACKEND_CONTAINER_PORT = os.getenv("BACKEND_CONTAINER_PORT", "5000")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_key_for_development')


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

    return jsonify({'confirmation': f'Admin {username} created successfully'}), 201

@app.route('/api/v1/admins/login', methods=['POST'])
def login_admin():
    data = request.get_json()
    admin = {"username": data['username'], "password": "hashed_password"}  #TODO: Actually get admin from database where username=data['username']

    if admin: # and check_password_hash(admin.password, data['password']):
        token_payload = {
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24),
            'iat': datetime.datetime.now(datetime.UTC),
            'sub': admin.username,  # Admin's username
            'role': 'admin'  # Admin role
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'])
        return jsonify({'jwt': token.decode('UTF-8')}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=BACKEND_CONTAINER_PORT)