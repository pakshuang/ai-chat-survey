from unittest import TestCase
from src.app import database_operations

class TestValidateSurveyObject(TestCase):
    def setUp(self):
        self.valid_data = {
            "metadata": {
                "created_by": "test_admin",
                "created_at": "2024-03-22 15:24:10",
            },
            "title": "Test Title",
            "subtitle": "Test Subtitle",
            "questions": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Which performance did you enjoy the most?",
                    "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
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
                    ],  # Empty list for open-ended question
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

    def test_valid_survey(self):
        result, message = database_operations.validate_survey_object(self.valid_data)
        self.assertTrue(result)
        self.assertEqual(message, "Survey object format is valid")

    def test_invalid_data_type(self):
        data = "This is not a dictionary"
        result, message = database_operations.validate_survey_object(data)
        self.assertFalse(result)
        self.assertEqual(message, "Survey data must be a dictionary")

    def test_missing_required_fields(self):
        data = {
            "title": "Test Title",
            "subtitle": "Test Subtitle",
            "questions": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Which performance did you enjoy the most?",
                    "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
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
                    ],  # Empty list for open-ended question
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
        result, message = database_operations.validate_survey_object(data)
        self.assertFalse(result)
        self.assertIn("metadata", message)

    def test_invalid_question_type(self):
        data = {
            "metadata": {
                "created_by": "test_admin",
                "created_at": "2024-03-22 15:24:10",
            },
            "title": "Test Title",
            "subtitle": "Test Subtitle",
            "questions": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Which performance did you enjoy the most?",
                    "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
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
                    ],  # Empty list for open-ended question
                },
                {
                    "question_id": 3,
                    "type": "long_answer",  # Invalid question type
                    "question": "Do you have any feedback about the venue?",
                    "options": [],  # Empty list for open-ended question
                },
            ],
            "chat_context": "Full Stack Entertainment is an events company that organises performances such as concerts.",
        }
        result, message = database_operations.validate_survey_object(data)
        self.assertFalse(result)
        self.assertEqual(message, "Invalid question type")

    def test_missing_question_keys(self):
        data = {
            "metadata": {
                "created_by": "test_admin",
                "created_at": "2024-03-22 15:24:10",
            },
            "title": "Test Title",
            "subtitle": "Test Subtitle",
            "questions": [
                {
                    "type": "multiple_choice",  # Missing question_id and question keys
                    "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
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
                    ],  # Empty list for open-ended question
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
        result, message = database_operations.validate_survey_object(data)
        self.assertFalse(result)
        self.assertIn("question_id", message)
        self.assertIn("question", message)

    def test_invalid_options_type(self):
        data = {
            "metadata": {
                "created_by": "test_admin",
                "created_at": "2024-03-22 15:24:10",
            },
            "title": "Test Title",
            "subtitle": "Test Subtitle",
            "questions": [
                {
                    "question_id": 1,
                    "type": "multiple_choice",
                    "question": "Which performance did you enjoy the most?",
                    "options": ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
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
                    ],  # Empty list for open-ended question
                },
                {
                    "question_id": 3,
                    "type": "free_response",
                    "question": "Do you have any feedback about the venue?",
                    "options": "",
                },
            ],
            "chat_context": "Full Stack Entertainment is an events company that organises performances such as concerts.",
        }
        result, message = database_operations.validate_survey_object(data)
        self.assertFalse(result)
        self.assertEqual(message, "Options field in a question must be a list")