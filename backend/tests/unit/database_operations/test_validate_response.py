from unittest import TestCase

from src.app import database_operations


class TestValidateResponse(TestCase):
    def test_valid_response_object(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Which performance did you enjoy the most?",
                    "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
                    "answer": ["Clowns"],
                },
                {
                    "question_id": 2,
                    "type": "multiple_response",
                    "question": "What did you like about the performance?",
                    "options": [
                        "This",
                        "Is",
                        "A",
                        "Test",
                    ],
                    "answer": ["A", "Test"],
                },
                {
                    "question_id": 3,
                    "type": "free_response",
                    "question": "Do you have any feedback about the venue?",
                    "options": [],
                    "answer": ["The venue was spacious and well-maintained."],
                },
            ],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertTrue(result)
        self.assertEqual(message, "Response object format is valid")

    def test_invalid_data_type(self):
        response_data = "This is not a dictionary"
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "Response data must be a dictionary")

    def test_missing_keys(self):
        response_data = {"missing_key": "value"}
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertIn("metadata", message)
        self.assertIn("answers", message)

    def test_invalid_metadata_type(self):
        response_data = {"metadata": "not_a_dict", "answers": []}
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'metadata' must be a dictionary")

    def test_missing_survey_id(self):
        response_data = {"metadata": {}, "answers": []}
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'metadata' must contain 'survey_id' key")

    def test_invalid_answers_type(self):
        response_data = {"metadata": {"survey_id": 3}, "answers": "not_a_list"}
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answers' must be a list")

    def test_invalid_answer_type(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Question 1",
                    "options": [],
                    "answer": "not_a_list",
                }
            ],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' must be a list")

    def test_empty_answer(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Question 1",
                    "options": [],
                    "answer": [],
                }
            ],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' is empty")

    def test_invalid_question_type(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [
                {
                    "question_id": 1,
                    "type": "invalid_type",
                    "question": "Question 1",
                    "options": [],
                    "answer": [],
                }
            ],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "Invalid question type")

    def test_missing_answer_keys(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [{"missing_key": "value"}],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertIn("question_id", message)

    def test_invalid_options_type(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Question 1",
                    "options": "not_a_list",
                    "answer": [],
                }
            ],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'options' must be a list")

    def test_invalid_answer_type(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Question 1",
                    "options": [],
                    "answer": "not_a_list",
                }
            ],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' must be a list")

    def test_empty_answer(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Question 1",
                    "options": [],
                    "answer": [],
                }
            ],
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' is empty")
