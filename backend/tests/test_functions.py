from ..src.llm_classes import  GPT, construct_chatlog, check_exit
from unittest import TestCase

class TestGPTFunctions(TestCase):
    FORMATTED = """
This survey is for Macdonald's, the fast food chain.
We are conducting a survey for the new seaweed shaker fries.


How satisfied are you with our product/service?

Options:
-    Very satisfied
-    Satisfied
-    Neutral
-    Dissatisfied
-    Very dissatisfied
Answer: Satisfied
How likely are you to recommend our product/service to others?

-   Very likely
-   Likely
-   Neutral
-   Unlikely
-   Very unlikely

Answer: Very likely
On a scale of 1 to 10, how would you rate the quality of our product/service?

Answer: 8
What do you like most about our product/service?

Answer: The ease of use and reliability.
What improvements would you suggest for our product/service?

Answer: More customization options and faster response times.
How often do you use our product/service?

-    Daily
-    Weekly
-    Monthly
-    Occasionally
-    Rarely
Answer: Weekly
How satisfied are you with the customer support provided?
Options:
-    Very satisfied
-    Satisfied
-    Neutral
-    Dissatisfied
-    Very dissatisfied
Answer: Satisfied
What made you choose our product/service over competitors?

Answer: Positive reviews and reputation.
How would you rate the value for money of our product/service?

Answer: 7
How easy was it to purchase/use our product/service?
Options:
-    Very easy
-    Easy
-    Neutral
-    Difficult
-    Very difficult
Answer: Easy
Would you consider purchasing from us again in the future?
Options:
-    Yes
-    No
-    Maybe
Answer: Yes
Overall, how satisfied are you with your experience with our company?
Options:
-    Very satisfied
-    Satisfied
-    Neutral
-    Dissatisfied
-    Very dissatisfied
Answer: Very satisfied
What improvements would you like to see in our company as a whole?

Answer: More frequent updates and better communication with customers.
How did you first hear about our company?
Options:
-    Word of mouth
-    Online advertisement
-    Social media
-    Other (please specify)

Answer: Word of mouth
Additional Comments:
Answer: Keep up the good work!


    """
    def test_check_exit_true(self):
        chatlog = construct_chatlog(TestGPTFunctions.FORMATTED, seed=120)
        chatlog.insert_and_update(
            "I wish to end the interview now. I do not want to cooperate. Please end it now.", chatlog.current_index
            )
        chatlog.insert_and_update(
            "Okay, understood. Thank you for your time, and goodbye!", chatlog.current_index, is_llm=True
            )
        seeds = [120, 240, 360]
        for seed in seeds:
            is_last = check_exit(chatlog.message_list, llm=GPT(), seed=seed)
            self.assertTrue(is_last)

    def test_check_exit_false(self):
        chatlog = construct_chatlog(TestGPTFunctions.FORMATTED, seed=120)
        chatlog.insert_and_update(
            "Hi, pleased to meet you! I have lots to share, but I would like to take another question. Is that okay?", chatlog.current_index
            )
        chatlog.insert_and_update(
            "Of course! Here is another question. What do you think about the Big Mac?", chatlog.current_index, is_llm=True
            )
        seeds = [120, 240, 360]
        for seed in seeds:
            is_last = check_exit(chatlog.message_list, llm=GPT(), seed=seed)
            self.assertFalse(is_last)



