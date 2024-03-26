from ..src.app import app

class TestFlaskApp:

    def setup_method(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_health_check(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.app.get('/api/v1/health')

        # assert the status code of the response
        assert response.status_code == 200

        # assert the response data
        assert b'Server is running!' in response.data
