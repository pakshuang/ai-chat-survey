from unittest import TestCase

from src.llm_classes.functions import (check_exit, construct_chatlog,
                                       format_multiple_choices,
                                       format_responses_for_gpt)
from src.llm_classes.llm_level import GPT


class TestGPTFunctions(TestCase):

    RESPONSE_FULL = {
        "metadata": {
            "survey_id": "integer",
            "response_id": "integer",
            "submitted_at": "string",
        },
        "answers": [
            {
                "question_id": "1",
                "type": "long",
                "question": "question?",
                "options": [""],
                "answer": ["string1 blah blah blah."],
            },
            {
                "question_id": "2",
                "type": "mrq",
                "question": "questionmrq?",
                "options": ["option 1", "option 2", "option 3"],
                "answer": ["option 1, option 2"],
            },
        ],
    }

    RESPONSE_LONG = {
        "metadata": {
            "survey_id": "integer",
            "response_id": "integer",
            "submitted_at": "string",
        },
        "answers": [
            {
                "question_id": "1",
                "type": "long",
                "question": "question?",
                "options": [""],
                "answer": ["string1 blah blah blah."],
            }
        ],
    }

    RESPONSE_MCQ = {
        "metadata": {
            "survey_id": "integer",
            "response_id": "integer",
            "submitted_at": "string",
        },
        "answers": [
            {
                "question_id": "1",
                "type": "mrq",
                "question": "question?",
                "options": ["option1", "option2", "option3"],
                "answer": ["string1", "string2"],
            }
        ],
    }

    FORMATTED = """
This survey is for Macdonald's, the fast food chain.
We are conducting a survey for the new seaweed shaker fries.

1. How satisfied are you with our product/service?
Options:
Very satisfied, Satisfied, Neutral, Dissatisfied, Very dissatisfied
Answer: Satisfied
2. How likely are you to recommend our product/service to others?
Very likely, Likely, Neutral, Unlikely, Very unlikely
Answer: Very likely
3. On a scale of 1 to 10, how would you rate the quality of our product/service?
Answer: 8
4. What do you like most about our product/service?
Answer: The ease of use and reliability.
5. What improvements would you suggest for our product/service?
Answer: More customization options and faster response times.
6. How often do you use our product/service?
Daily, Weekly, Monthly, Rarely
Answer: Weekly
7. How satisfied are you with the customer support provided?
Options:
Very Satisfied, Satisfied, Neutral, Unsatisfied, Very unsatisfied
Answer: Satisfied
8. What made you choose our product/service over competitors?
Answer: Positive reviews and reputation.
9. How would you rate the value for money of our product/service?
Answer: 7
10. How easy was it to purchase/use our product/service?
Options:
Very easy, Easy, Neutral, Difficult, Very difficult
Answer: Easy
11. Would you consider purchasing from us again in the future?
Options:
Yes, No, Maybe
Answer: Yes
12. Overall, how satisfied are you with your experience with our company?
Options:
Very Satisfied, Satisfied, Neutral, Unsatisfied, Very unsatisfied
Answer: Very satisfied
13. What improvements would you like to see in our company as a whole?
Answer: More frequent updates and better communication with customers.
14. How did you first hear about our company?
Options:
Word of mouth, Online advertisement, Social media, Other (please specify)
Answer: Word of mouth
15. Additional Comments:
Answer: Keep up the good work!

    """

    def test_check_exit_true(self):
        chatlog = construct_chatlog(TestGPTFunctions.FORMATTED, seed=120)
        chatlog.insert_and_update(
            "I wish to end the interview now. I do not want to cooperate. Please end it now.",
            chatlog.current_index,
        )
        chatlog.insert_and_update(
            "Okay, understood. Thank you for your time, and goodbye!",
            chatlog.current_index,
            is_llm=True,
        )
        seeds = [120, 240]
        for seed in seeds:
            is_last = check_exit(chatlog.message_list, llm=GPT(), seed=seed)
            assert is_last

    def test_check_exit_many(self):

        seed = 120
        chatlog = construct_chatlog(TestGPTFunctions.FORMATTED, seed=seed)
        chatlog.insert_and_update(
            "Hi, pleased to meet you! I have lots to share, but I would like to take another question. Is that okay?",
            chatlog.current_index,
        )
        self.assertTrue(len(chatlog), 4)
        for i in range(13):
            chatlog.insert_and_update(
                "Of course! Here is another question. Why are you satisfied but not very satisfied with our products?",
                chatlog.current_index,
                is_llm=True,
            )
            chatlog.insert_and_update(
                "It doesnt really taste very good. I want to continue the interview, next question please.",
                chatlog.current_index,
            )
        self.assertEqual(len(chatlog), 30)
        boolean = check_exit(chatlog.message_list, llm=chatlog.llm, seed=seed)
        self.assertFalse(boolean)

        chatlog.insert_and_update(
            "Of course! Here is another question. Why are you satisfied but not very satisfied with our products?",
            chatlog.current_index,
            is_llm=True,
        )

        boolean = check_exit(chatlog.message_list, llm=chatlog.llm, seed=seed)
        self.assertTrue(boolean)
        self.assertTrue(len(chatlog) > 30)

    def test_check_exit_false(self):
        chatlog = construct_chatlog(TestGPTFunctions.FORMATTED, seed=120)
        chatlog.insert_and_update(
            "Hi, pleased to meet you! I have lots to share, but I would like to take another question. Is that okay?",
            chatlog.current_index,
        )
        chatlog.insert_and_update(
            "Of course! Here is another question. What do you think about the Big Mac?",
            chatlog.current_index,
            is_llm=True,
        )
        seeds = [120, 240]
        for seed in seeds:
            is_last = check_exit(chatlog.message_list, llm=GPT(), seed=seed)
            self.assertFalse(is_last)

    def test_check_format_format_multiple_choice(self):
        options = TestGPTFunctions.RESPONSE_MCQ["answers"][0]["options"]
        answer = TestGPTFunctions.RESPONSE_MCQ["answers"][0]["answer"]
        self.assertIn("Options:\n", format_multiple_choices(options, "Option"))
        self.assertEqual(
            "Options:\noption1, option2, option3",
            format_multiple_choices(options, "Option"),
        )
        self.assertIn("Answers:\n", format_multiple_choices(answer, "Answer"))
        self.assertEqual(
            "Dog:\noption1.option2.option3",
            format_multiple_choices(options, "Dog", add_plural=False, sep="."),
        )

    def test_check_format_long_ans(self):
        options = TestGPTFunctions.RESPONSE_LONG["answers"][0]["options"]
        answer = TestGPTFunctions.RESPONSE_LONG["answers"][0]["answer"]

        self.assertTrue(not format_multiple_choices(options, "Option"))
        self.assertEqual(
            "Answer:\nstring1 blah blah blah.",
            format_multiple_choices(answer, "Answer"),
        )

    def test_check_format_responses_for_gpt(self):
        comparer = """1. question?\nOptions:\noption1, option2, option3\nAnswers:\nstring1, string2"""
        self.assertEqual(
            format_responses_for_gpt(TestGPTFunctions.RESPONSE_MCQ), comparer
        )
        comparer_long = """1. question?\n\nAnswer:\nstring1 blah blah blah."""
        self.assertEqual(
            format_responses_for_gpt(TestGPTFunctions.RESPONSE_LONG), comparer_long
        )
        comparer_full = """1. question?\n\nAnswer:\nstring1 blah blah blah.\n2. questionmrq?\nOptions:\noption1, option2, option3\nAnswers:\noption1, option2"""
