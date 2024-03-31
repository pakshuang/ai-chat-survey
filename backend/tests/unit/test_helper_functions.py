from datetime import datetime
from unittest import TestCase
from src.app import database_operations

class TestHelperFunctions(TestCase):
    def test_valid_survey(self):
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
                    "options": [],  # Empty list for open-ended question
                },
            ],
            "chat_context": "Full Stack Entertainment is an events company that organises performances such as concerts.",
        }
        result, message = database_operations.validate_survey_object(data)
        print(message)
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
                    "type": "long_answer",
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
    def test_create_survey_object(self):
        row = {
            "survey_id": 123,
            "admin_username": "admin",
            "created_at": datetime(2024, 3, 31, 12, 0, 0),
            "title": "Survey Title",
            "subtitle": "Survey Subtitle",
            "chat_context": {"key": "value"}
        }
        expected_survey_object = {
            "metadata": {
                "survey_id": 123,
                "created_by": "admin",
                "created_at": "2024-03-31 12:00:00"
            },
            "title": "Survey Title",
            "subtitle": "Survey Subtitle",
            "questions": [],
            "chat_context": {"key": "value"}
        }
        result = database_operations.create_survey_object(row)
        self.assertEqual(result, expected_survey_object)

    def test_append_question_to_survey(self):
        # Sample survey objects dictionary
        survey_objects = {
            1: {
                "metadata": {"survey_id": 1},
                "questions": []
            },
            2: {
                "metadata": {"survey_id": 2},
                "questions": []
            }
        }

        # Sample question data
        question_data = {
            "question_id": 1,
            "question_type": "multiple_choice",
            "question": "What is your favorite color?",
            "options": '["Red", "Blue", "Green"]'
        }

        # Append question to survey 1
        database_operations.append_question_to_survey(survey_objects, 1, question_data)

        # Check if the question is correctly appended to survey 1
        self.assertEqual(len(survey_objects[1]["questions"]), 1)
        self.assertEqual(survey_objects[1]["questions"][0]["question_id"], 1)
        self.assertEqual(survey_objects[1]["questions"][0]["type"], "multiple_choice")
        self.assertEqual(survey_objects[1]["questions"][0]["question"], "What is your favorite color?")
        self.assertEqual(survey_objects[1]["questions"][0]["options"], ["Red", "Blue", "Green"])

        # Append question to survey 2
        database_operations.append_question_to_survey(survey_objects, 2, question_data)

        # Check if the question is correctly appended to survey 2
        self.assertEqual(len(survey_objects[2]["questions"]), 1)
        self.assertEqual(survey_objects[2]["questions"][0]["question_id"], 1)
        self.assertEqual(survey_objects[2]["questions"][0]["type"], "multiple_choice")
        self.assertEqual(survey_objects[2]["questions"][0]["question"], "What is your favorite color?")
        self.assertEqual(survey_objects[2]["questions"][0]["options"], ["Red", "Blue", "Green"])

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
            "answers": [{"question_id": 1, "type": "multiple_choice", "question": "Question 1", "options": [], "answer": "not_a_list"}]
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' must be a list")

    def test_empty_answer(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [{"question_id": 1, "type": "multiple_choice", "question": "Question 1", "options": [], "answer": []}]
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' is empty")

    def test_invalid_question_type(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [{"question_id": 1, "type": "invalid_type", "question": "Question 1", "options": [], "answer": []}]
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "Invalid question type")

    def test_missing_answer_keys(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [{"missing_key": "value"}]
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertIn("question_id", message)

    def test_invalid_options_type(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [{"question_id": 1, "type": "multiple_choice", "question": "Question 1", "options": "not_a_list", "answer": []}]
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'options' must be a list")

    def test_invalid_answer_type(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [{"question_id": 1, "type": "multiple_choice", "question": "Question 1", "options": [], "answer": "not_a_list"}]
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' must be a list")

    def test_empty_answer(self):
        response_data = {
            "metadata": {"survey_id": 3},
            "answers": [{"question_id": 1, "type": "multiple_choice", "question": "Question 1", "options": [], "answer": []}]
        }
        result, message = database_operations.validate_response_object(response_data)
        self.assertFalse(result)
        self.assertEqual(message, "'answer' is empty")