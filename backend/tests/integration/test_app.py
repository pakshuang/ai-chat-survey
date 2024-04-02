import datetime
import os
import requests

import jwt

BACKEND_URL = "http://backend:" + os.getenv("BACKEND_CONTAINER_PORT")


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

    assert response.json() == {"message": "Admin admin1 created successfully"}
    assert response.status_code == 201


def test_create_admin_second_success():
    response = requests.post(
        ADMINS_ENDPOINT,
        json={"username": "admin2", "password": "password2"},
    )

    assert response.json() == {"message": "Admin admin2 created successfully"}
    assert response.status_code == 201


def test_create_admin_existing_admin():
    response = requests.post(
        ADMINS_ENDPOINT,
        json={"username": "admin1", "password": "password2"},
    )

    assert response.json() == {"message": "Admin already exists"}
    assert response.status_code == 400


def test_create_admin_missing_data():
    response = requests.post(ADMINS_ENDPOINT, json={})

    assert response.status_code == 400
    assert response.json() == {"message": "Missing data"}


def test_create_admin_missing_username():
    response = requests.post(ADMINS_ENDPOINT, json={"password": "password1"})

    assert response.status_code == 400
    assert response.json() == {"message": "Missing data"}


def test_create_admin_missing_password():
    response = requests.post(ADMINS_ENDPOINT, json={"username": "admin1"})

    assert response.status_code == 400
    assert response.json() == {"message": "Missing data"}


# Test cases for login_admin

VALID_JWT = ""
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "default_key_for_development")


def test_admin_login_success():
    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin1", "password": "password1"},
    )
    token_payload = {
                    "exp": datetime.datetime.now(datetime.UTC)
                    + datetime.timedelta(hours=24),
                    "iat": datetime.datetime.now(datetime.UTC),
                    "sub": "admin1",  # Admin's username
                }
    token = jwt.encode(
                    token_payload, FLASK_SECRET_KEY, algorithm="HS256"
                )
    expected_response = {
                            "jwt": token,
                            "jwt_exp": token_payload["exp"].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    
    assert response.status_code == 200
    assert response.json() == expected_response

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
            "options": ["Seating", "Lighting", "Sound"],
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
    headers = {"Authorization": "Bearer " + "INVALID_JWT"}
    response = requests.post(SURVEYS_ENDPOINT, json=SURVEY_DATA, headers=headers)

    print(response.json())
    assert response.status_code == 401
    assert response.json().get("message") == "Token is invalid!"


def test_create_survey_missing_jwt():
    response = requests.post(SURVEYS_ENDPOINT, json=SURVEY_DATA)

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Token is missing!"


# Test cases for get_surveys


def test_get_surveys_success():
    response = requests.get(SURVEYS_ENDPOINT)

    global SURVEY_DATA
    SURVEY_DATA["metadata"]["survey_id"] = SURVEY_ID

    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert SURVEY_DATA in response.json()


def test_get_surveys_filtered_success():
    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin2", "password": "password2"},
    )
    admin2_jwt = response.json().get("jwt")

    headers = {"Authorization": "Bearer " + admin2_jwt}

    survey_data = {
        "metadata": {
            "created_by": "admin2",
            "created_at": "2024-03-22 15:25:10",
        },
        "title": "Another Title",
        "subtitle": "Another Subtitle",
        "questions": [
            {
                "question_id": 1,
                "type": "multiple_response",
                "question": "Which cheeses do you like?",
                "options": ["Cheddar", "Brie", "Gouda"],
            },
            {
                "question_id": 2,
                "type": "multiple_choice",
                "question": "Cheese or chocolate?",
                "options": ["Cheese", "Chocolate"],
            },
            {
                "question_id": 3,
                "type": "free_response",
                "question": "Why?",
                "options": [],
            },
        ],
        "chat_context": "We are a cheese company.",
    }

    requests.post(SURVEYS_ENDPOINT, json=survey_data, headers=headers)

    response = requests.get(SURVEYS_ENDPOINT + "?admin=admin1")

    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert SURVEY_DATA in response.json()


def test_get_surveys_empty_success():
    response = requests.get(SURVEYS_ENDPOINT + "?admin=admin3")

    print(response.json())
    assert response.status_code == 200


# Test cases for get_survey<survey_id>


def test_get_survey_success():
    response = requests.get(SURVEYS_ENDPOINT + "/" + str(SURVEY_ID))

    print(response.json())
    assert response.status_code == 200
    assert response.json() == SURVEY_DATA


def test_get_survey_not_found():
    response = requests.get(SURVEYS_ENDPOINT + "/0")

    print(response.json())
    assert response.status_code == 404
    assert response.json().get("message") == "Survey not found"


# Test cases for delete_survey<survey_id>


def test_delete_survey_success():
    response = requests.get(SURVEYS_ENDPOINT + "?admin=admin2")
    admin2_survey_id = response.json()[0].get("metadata").get("survey_id")

    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin2", "password": "password2"},
    )
    admin2_jwt = response.json().get("jwt")

    headers = {"Authorization": "Bearer " + admin2_jwt}
    response = requests.delete(
        SURVEYS_ENDPOINT + "/" + str(admin2_survey_id), headers=headers
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json().get("message") == "Survey deleted successfully"

    response = requests.get(SURVEYS_ENDPOINT + "?admin=admin2")
    assert len(response.json()) == 0


def test_delete_survey_missing_jwt():
    response = requests.delete(SURVEYS_ENDPOINT + "/1")

    print(response.json())
    assert response.status_code == 400
    assert response.json().get("message") == "Token is missing!"


def test_delete_survey_unauthorized():
    headers = {"Authorization": "Bearer " + "INVALID_JWT"}
    response = requests.delete(SURVEYS_ENDPOINT + "/1", headers=headers)

    print(response.json())
    assert response.status_code == 401
    assert response.json().get("message") == "Token is invalid!"


def test_delete_survey_wrong_admin():
    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin2", "password": "password2"},
    )
    admin2_jwt = response.json().get("jwt")

    headers = {"Authorization": "Bearer " + admin2_jwt}
    response = requests.delete(SURVEYS_ENDPOINT + "/1", headers=headers)

    print(response.json())
    assert response.status_code == 403
    assert (
        response.json().get("message") == "Accessing other admin's surveys is forbidden"
    )


def test_delete_survey_not_found():
    response = requests.post(
        ADMINS_ENDPOINT + "/login",
        json={"username": "admin2", "password": "password2"},
    )
    admin2_jwt = response.json().get("jwt")

    headers = {"Authorization": "Bearer " + admin2_jwt}
    response = requests.delete(SURVEYS_ENDPOINT + "/0", headers=headers)

    print(response.json())
    assert response.status_code == 404
    assert response.json().get("message") == "Survey not found"
