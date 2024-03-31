from datetime import datetime
from unittest import TestCase
from src.app import database_operations


class TestCreateResponse(TestCase):
    def test_create_response_object(self):
        row = {"submitted_at": datetime(2024, 3, 31, 12, 0, 0)}
        expected_response_object = {
            "metadata": {
                "survey_id": 1,
                "response_id": 123,
                "submitted_at": "2024-03-31 12:00:00",
            },
            "answers": [],
        }
        result = database_operations.create_response_object(1, 123, row)
        self.assertEqual(result, expected_response_object)

    def test_append_answer_to_response(self):
        # Sample response objects dictionary
        response_objects = {
            123: {
                "metadata": {
                    "survey_id": 1,
                    "response_id": 123,
                    "submitted_at": "2024-03-31 12:00:00",
                },
                "answers": [],
            }
        }

        # Sample response data
        response_data = {
            "question_id": 1,
            "question_type": "multiple_choice",
            "question": "What is your favorite color?",
            "options": '["Red", "Blue", "Green"]',
            "answer": '["Blue"]',
        }

        # Append answer to response 1
        database_operations.append_answer_to_response(
            response_objects, 123, response_data
        )

        # Check if the answer is correctly appended to response 1
        self.assertEqual(len(response_objects[123]["answers"]), 1)
        self.assertEqual(response_objects[123]["answers"][0]["question_id"], 1)
        self.assertEqual(response_objects[123]["answers"][0]["type"], "multiple_choice")
        self.assertEqual(
            response_objects[123]["answers"][0]["question"],
            "What is your favorite color?",
        )
        self.assertEqual(
            response_objects[123]["answers"][0]["options"], ["Red", "Blue", "Green"]
        )
        self.assertEqual(response_objects[123]["answers"][0]["answer"], ["Blue"])
