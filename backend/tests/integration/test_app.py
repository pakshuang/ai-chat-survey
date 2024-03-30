import os
import requests

class TestFlaskApp:

    BACKEND_URL = "http://" + "backend" + ":" + os.getenv("BACKEND_CONTAINER_PORT")

    def test_health_check(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = requests.get(TestFlaskApp.BACKEND_URL + "/api/v1/health")

        # assert the status code of the response
        assert response.status_code == 200

    # # Test cases for creating admins

    # def test_create_admin_success(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with valid data
    #     response = self.app.post(
    #         "/api/v1/admins", json={"username": "admin1", "password": "password1"}
    #     )

    #     # assert the status code of the response
    #     assert response.status_code == 201

    # def test_create_admin_second_success(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with valid data
    #     response = self.app.post(
    #         "/api/v1/admins", json={"username": "admin2", "password": "password2"}
    #     )

    #     # assert the status code of the response
    #     assert response.status_code == 201

    # def test_create_admin_existing_admin(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with existing admin data
    #     response = self.app.post(
    #         "/api/v1/admins", json={"username": "admin1", "password": "password2"}
    #     )

    #     # assert the status code of the response
    #     assert response.status_code == 400

    # def test_create_admin_missing_data(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with missing data
    #     response = self.app.post("/api/v1/admins", json={})

    #     # assert the status code of the response
    #     assert response.status_code == 400

    # def test_create_admin_missing_username(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with invalid data
    #     response = self.app.post("/api/v1/admins", json={"password": "password1"})

    #     # assert the status code of the response
    #     assert response.status_code == 400

    # def test_create_admin_missing_password(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with invalid data
    #     response = self.app.post("/api/v1/admins", json={"username": "admin1"})

    #     # assert the status code of the response
    #     assert response.status_code == 400

    # # Test cases for admin login

    # valid_jwt = ""

    # def test_admin_login_success(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with valid data
    #     response = self.app.post(
    #         "/api/v1/admins/login", json={"username": "admin1", "password": "password1"}
    #     )

    #     # assert the status code of the response
    #     assert response.status_code == 200

    #     # assert the response data
    #     assert b"jwt" in response.data
    #     assert b"jwt_exp" in response.data

    #     # set the valid jwt token
    #     self.valid_jwt = response.json["jwt"]

    # def test_admin_login_missing_data(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with missing data
    #     response = self.app.post("/api/v1/admins/login", json={})

    #     # assert the status code of the response
    #     assert response.status_code == 400

    # def test_admin_login_missing_username(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with invalid data
    #     response = self.app.post("/api/v1/admins/login", json={"password": "password1"})

    #     # assert the status code of the response
    #     assert response.status_code == 400

    # def test_admin_login_missing_password(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with invalid data
    #     response = self.app.post("/api/v1/admins/login", json={"username": "admin1"})

    #     # assert the status code of the response
    #     assert response.status_code == 400

    # def test_admin_login_invalid_username(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with invalid data
    #     response = self.app.post(
    #         "/api/v1/admins/login", json={"username": "admin3", "password": "password1"}
    #     )

    #     # assert the status code of the response
    #     assert response.status_code == 401

    # def test_admin_login_invalid_password(self):
    #     # sends HTTP POST request to the application
    #     # on the specified path with invalid data
    #     response = self.app.post(
    #         "/api/v1/admins/login", json={"username": "admin1", "password": "password2"}
    #     )

    #     # assert the status code of the response
    #     assert response.status_code == 401
