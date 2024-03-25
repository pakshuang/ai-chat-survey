import requests
import time

def test_create_admin():
    url = "http://localhost:{}/api/v1/admins".format(
        "5000"
    )  # Assuming BACKEND_CONTAINER_PORT is defined
    data = {"username": "test_admin", "password": "test_password"}
    response = requests.post(url, json=data)
    print(response)
    # Print the response content
    print("Response content:", response.json())
    # assert response.status_code == 201
    # assert response.json()["message"] == "Admin test_admin created successfully"


def test_login_admin():
    url = "http://localhost:{}/api/v1/admins/login".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    data = {"username": "test_admin", "password": "test_password"}
    response = requests.post(url, json=data)
    print(response)

    # Print the response content
    print("Response content:", response.json())
    # assert response.status_code == 200
    # assert "jwt" in response.json()  # Check if JWT token is returned in the response


def test_create_survey():
    create_survey_url = "http://localhost:{}/api/v1/surveys".format(
        "5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    login_url = "http://localhost:{}/api/v1/admins/login".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined

    # Login first
    login_data = {"username": "test_admin", "password": "test_password"}
    login_response = requests.post(login_url, json=login_data)
    jwt_token = login_response.json().get('jwt')

    # assert jwt_token, "JWT token not obtained"

    # Sample survey data
    survey_data = {
        "metadata": {
            "id": 1,
            "name": "Test Survey",
            "description": "This is a test survey",
            "created_by": "test_admin",
            "created_at": "2024-03-22 15:24:10"
        },
        "title": "Test Title",
        "subtitle": "Test Subtitle",
        "questions": [
            {
                "id": 1,
                "type": "multiple_choice",
                "question": "Which performance did you enjoy the most?",
                "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"]
            },
            {
                "id": 2,
                "type": "short_answer",
                "question": "What did you like about the performance?",
                "options": []  # Empty list for open-ended question
            },
            {
                "id": 3,
                "type": "long_answer",
                "question": "Do you have any feedback about the venue?",
                "options": []  # Empty list for open-ended question
            }
        ],
        "chat_context": "Full Stack Entertainment is an events company that organises performances such as concerts."
    }

    headers = {
        "Authorization": "Bearer " + jwt_token
    }

    # Create a survey
    create_survey_response = requests.post(create_survey_url, json=survey_data, headers=headers)

    # Assertions
    # assert create_survey_response.status_code == 201, "Survey creation failed"
    # assert "survey_id" in create_survey_response.json(), "Survey ID not returned"
    print("Survey created successfully. Survey ID:", create_survey_response.json()["survey_id"])


def test_get_surveys():
    url = ("http://localhost:{}/api/v1/surveys").format(
        "5000")  # Assuming BACKEND_CONTAINER_PORT is defined

    print(url)
    # Send GET request to get surveys
    response = requests.get(url)

    # Print the response content
    print(response.json())

    # Assert the status code
    # assert response.status_code == 400 or response.status_code == 200


def test_get_survey():
    url = "http://localhost:{}/api/v1/surveys/3".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    print(url)

    # Send GET request to get surveys
    response = requests.get(url)
    print(response)
    # Print the response content
    print(response.json())

    # Assert the status code
    # assert response.status_code == 400 or response.status_code == 200


def test_delete_survey():
    login_url = "http://localhost:{}/api/v1/admins/login".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    # Login first
    data = {"username": "test_admin", "password": "test_password"}
    response = requests.post(login_url, json=data)

    # Get jwt token
    jwt_token = response.json()['jwt']
    print(jwt_token)

    headers = {
        "Authorization": "Bearer " + jwt_token  # Include your admin token here
    }

    # URL for deleting a survey
    delete_survey_url = "http://localhost:{}/api/v1/surveys/3".format("5000")
    # Assuming you already have a valid survey_id for testing

    # Send DELETE request to delete the survey
    response = requests.delete(delete_survey_url, headers=headers)

    # Print the response content
    print(response.json())

    # Assert the status code
    # assert response.status_code == 200
    # assert response.json()["message"] == "Survey deleted successfully"

    # Check if the survey is deleted from the database
    # You can perform additional checks here to ensure associated questions and responses are deleted as well

def test_submit_response():
    # Define the URL for submitting responses
    url = "http://localhost:{}/api/v1/responses".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined

    # Sample response data with correct structure and values
    response_data = {
        "metadata": {
            "survey_id": 3
        },
        "answers": [
            {
                "question_id": 1,
                "type": "multiple_choice",
                "question": "Which performance did you enjoy the most?",
                "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
                "answer": "Clowns"
            },
            {
                "question_id": 2,
                "type": "short_answer",
                "question": "What did you like about the performance?",
                "options": [],  # Empty list provided for short answer question
                "answer": "I enjoyed the acrobatic stunts."
            },
            {
                "question_id": 3,
                "type": "long_answer",
                "question": "Do you have any feedback about the venue?",
                "options": [],  # Empty list provided for long answer question
                "answer": "The venue was spacious and well-maintained."
            }
        ]
    }

    # Send POST request to submit response
    response = requests.post(url, json=response_data)
    print(response.json())
    # # Assert the status code and response message
    # assert response.status_code == 201
    # assert "response_id" in response.json()

def test_get_responses():
    url = "http://localhost:{}/api/v1/responses".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    survey_id = 3  # Assuming the survey ID for testing
    login_url = "http://localhost:{}/api/v1/admins/login".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    # Login first
    data = {"username": "test_admin", "password": "test_password"}
    response = requests.post(login_url, json=data)

    # Get jwt token
    jwt_token = response.json()['jwt']
    print(jwt_token)

    headers = {
        "Authorization": "Bearer " + jwt_token  # Include your admin token here
    }

    # Send GET request to get responses for the survey
    response = requests.get(url, params={"survey": survey_id}, headers=headers)
    print(response.json())


def test_get_response():
    url = "http://localhost:{}/api/v1/responses/{}?survey={}".format("5000", 1, 3)

    login_url = "http://localhost:{}/api/v1/admins/login".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    # Login first
    data = {"username": "test_admin", "password": "test_password"}
    response = requests.post(login_url, json=data)

    # Get jwt token
    jwt_token = response.json()['jwt']
    print(jwt_token)

    headers = {
        "Authorization": "Bearer " + jwt_token  # Include your admin token here
    }

    # Send GET request to get responses for the survey
    response = requests.get(url, headers=headers)
    print(response.json())

def test_send_chat_message():
    url = "http://localhost:{}/api/v1/responses/{}/chat?survey={}".format("5000", 1, 3)

    login_url = "http://localhost:{}/api/v1/admins/login".format("5000")  # Assuming BACKEND_CONTAINER_PORT is defined
    # Login first
    data = {"username": "test_admin", "password": "test_password"}
    response = requests.post(login_url, json=data)

    # Get jwt token
    jwt_token = response.json()['jwt']

    headers = {
        "Authorization": "Bearer " + jwt_token,  # Include your admin token here
        "Content-Type": "application/json"
    }

    # Prepare response data
    response_data = {
        "content": "Please be correct"
    }

    # Send POST request to send chat message
    response = requests.post(url, json=response_data, headers=headers)
    print(response.json())

    # Check if the response is successful
    # assert response.status_code == 201
    # Add more assertions based on your expected behavior
    # Example: assert response.json()["content"] == "Expected content"

if __name__ == "__main__":
    test_create_admin()
    test_create_survey()
    test_get_surveys()
    test_get_survey()
    test_submit_response()
    test_get_responses()
    test_get_response()
    test_send_chat_message()

    # test_delete_survey()