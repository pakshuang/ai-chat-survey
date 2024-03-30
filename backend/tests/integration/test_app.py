import os

import requests


class TestFlaskApp:

    BACKEND_URL = "http://" + "backend" + ":" + os.getenv("BACKEND_CONTAINER_PORT")

    def test_health_check(self):
        response = requests.get(TestFlaskApp.BACKEND_URL + "/api/v1/health")

        print(response.json())
        assert response.status_code == 200

    ADMINS_ENDPOINT = BACKEND_URL + "/api/v1/admins"

    # Test cases for create_admin

    def test_create_admin_success(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT,
            json={"username": "admin1", "password": "password1"},
        )

        print(response.json())
        assert response.status_code == 201

    def test_create_admin_second_success(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT,
            json={"username": "admin2", "password": "password2"},
        )

        print(response.json())
        assert response.status_code == 201

    def test_create_admin_existing_admin(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT,
            json={"username": "admin1", "password": "password2"},
        )

        print(response.json())
        assert response.status_code == 400
        assert response.json().get("message") == "Admin already exists"

    def test_create_admin_missing_data(self):
        response = requests.post(TestFlaskApp.ADMINS_ENDPOINT, json={})

        print(response.json())
        assert response.status_code == 400
        assert response.json().get("message") == "Missing data"

    def test_create_admin_missing_username(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT, json={"password": "password1"}
        )

        print(response.json())
        assert response.status_code == 400
        assert response.json().get("message") == "Missing data"

    def test_create_admin_missing_password(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT, json={"username": "admin1"}
        )

        print(response.json())
        assert response.status_code == 400
        assert response.json().get("message") == "Missing data"

    # Test cases for login_admin

    def test_admin_login_success(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT + "/login",
            json={"username": "admin1", "password": "password1"},
        )

        print(response.json())
        assert response.status_code == 200
        assert "jwt" in response.json()
        assert "jwt_exp" in response.json()

        # set the valid jwt token
        self.valid_jwt = response.json().get("jwt")

    def test_admin_login_missing_data(self):
        response = requests.post(TestFlaskApp.ADMINS_ENDPOINT + "/login", json={})

        print(response.json())
        assert response.status_code == 400
        assert response.json().get("message") == "Missing data"

    def test_admin_login_missing_username(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT + "/login",
            json={"password": "password1"},
        )

        print(response.json())
        assert response.status_code == 400
        assert response.json().get("message") == "Missing data"

    def test_admin_login_missing_password(self):

        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT + "/login",
            json={"username": "admin1"},
        )

        print(response.json())
        assert response.status_code == 400
        assert response.json().get("message") == "Missing data"

    def test_admin_login_invalid_username(self):

        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT + "/login",
            json={"username": "admin3", "password": "password1"},
        )

        print(response.json())
        assert response.status_code == 401
        assert response.json().get("message") == "Invalid credentials"

    def test_admin_login_wrong_password(self):
        response = requests.post(
            TestFlaskApp.ADMINS_ENDPOINT + "/login",
            json={"username": "admin1", "password": "password2"},
        )

        print(response.json())
        assert response.status_code == 401
        assert response.json().get("message") == "Invalid credentials"
