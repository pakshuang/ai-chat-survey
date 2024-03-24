import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from backend.src.app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_health_check(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.app.get('/api/v1/health')

        # assert the status code of the response
        self.assertEqual(response.status_code, 200)

        # assert the response data
        self.assertIn(b'Server is running!', response.data)