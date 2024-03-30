import os

import requests


BACKEND_URL = "http://" + "backend" + ":" + os.getenv("BACKEND_CONTAINER_PORT")


def test_health_check():
    response = requests.get(BACKEND_URL + "/api/v1/health")

    print(response.json())
    assert response.status_code == 200


# Test cases for create_admin

ADMINS_ENDPOINT = BACKEND_URL + "/api/v1/admins"


def test_create_admin_success():
    response = requests.post(
        ADMINS_ENDPOINT,
        json={"username": "admin1", "password": "password1"},
    )

    print(response.json())
    assert response.status_code == 201


def test_create_admin_second_success():
    response = requests.post(
        ADMINS_ENDPOINT,
        json={"username": "admin2", "password": "password2"},
    )

    print(response.json())
    assert response.status_code == 201


def test_create_admin_existing_admin():
    response = requests.post(
        ADMINS_ENDPOINT,
        json={"username": "admin1", "password": "password2"},
    )

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Admin already exists"


def test_create_admin_missing_data():
    response = requests.post(ADMINS_ENDPOINT, json={})

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing data"


def test_create_admin_missing_username():
    response = requests.post(ADMINS_ENDPOINT, json={"password": "password1"})

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing data"


def test_create_admin_missing_password():
    response = requests.post(ADMINS_ENDPOINT, json={"username": "admin1"})

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing data"


# Test cases for login_admin

VALID_JWT = ""


def test_admin_login_success():
    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin1", "password": "password1"},
    )

    print(response.json())
    assert response.status_code == 200
    assert "jwt" in response.json()
    assert "jwt_exp" in response.json()

    # set the valid jwt token
    global VALID_JWT
    VALID_JWT = response.json().get("jwt")


def test_admin_login_missing_data():
    response = requests.post(ADMINS_ENDPOINT + "/login", json={})

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing data"


def test_admin_login_missing_username():
    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"password": "password1"},
    )

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing data"


def test_admin_login_missing_password():

    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin1"},
    )

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing data"


def test_admin_login_invalid_username():

    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin3", "password": "password1"},
    )

    print(response.json())
    assert response.status_code == 401
    assert response.json().get("message") == "Invalid credentials"


def test_admin_login_wrong_password():
    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin1", "password": "password2"},
    )

    print(response.json())
    assert response.status_code == 401
    assert response.json().get("message") == "Invalid credentials"


# Test cases for create_survey

SURVEYS_ENDPOINT = BACKEND_URL + "/api/v1/surveys"
SURVEY_ID = 0
SURVEY_DATA = {
    "metadata": {
        "created_by": "admin1",
        "created_at": "2024-03-22 15:24:10",
    },
    "title": "Test Title",
    "subtitle": "Test Subtitle",
    "questions": [
        {
            "question_id": 1,
            "type": "multiple_choice",
            "question": "Which performance did you enjoy the most?",
            "options": ["Clowns", "Acrobats", "Jugglers", "Magicians"],
        },
        {
            "question_id": 2,
            "type": "multiple_response",
            "question": "What did you like about the venue?",
            "options": [
                "Ambience",
                "Aircon",
                "Decor",
                "Vibe",
            ],
        },
        {
            "question_id": 3,
            "type": "free_response",
            "question": "Do you have any feedback about the venue?",
            "options": [],  # Empty list for open-ended question
        },
    ],
    "chat_context": "Full Stack Entertainment is an events company that organises performances such as concerts.",
}


def test_create_survey_success():
    headers = {"Authorization": "Bearer " + VALID_JWT}

    response = requests.post(SURVEYS_ENDPOINT, json=SURVEY_DATA, headers=headers)

    print(response.json())
    assert response.status_code == 201
    assert "survey_id" in response.json()
    global SURVEY_ID
    SURVEY_ID = response.json().get("survey_id")


def test_create_survey_missing_data():
    headers = {"Authorization": "Bearer " + VALID_JWT}

    response = requests.post(SURVEYS_ENDPOINT, json={}, headers=headers)

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing data"


def test_create_survey_missing_metadata():
    survey_data = SURVEY_DATA.copy()
    survey_data.pop("metadata")

    headers = {"Authorization": "Bearer " + VALID_JWT}

    response = requests.post(SURVEYS_ENDPOINT, json=survey_data, headers=headers)

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Missing or empty 'metadata' field"


def test_create_survey_unauthorized():
    headers = {"Authorization ": "Bearer " + "INVALID_JWT"}

    response = requests.post(SURVEYS_ENDPOINT, json=SURVEY_DATA, headers=headers)

    print(response.json())
    assert response.status_code == 401
    assert response.json().get("message") == "Unauthorized"


def test_create_survey_missing_jwt():
    response = requests.post(SURVEYS_ENDPOINT, json=SURVEY_DATA)

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Token is missing!"
