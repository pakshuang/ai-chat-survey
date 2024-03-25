from chatlog import LLM, GPT, ChatLog

def construct_chatlog(survey_initial_responses: str, llm: LLM = GPT()) -> ChatLog:
    start_dict = {
            "role": "system",
            "content": ChatLog.SYSPROMPT.format(
                survey_initial_responses=survey_initial_responses
            ),
        }
    return ChatLog([start_dict], llm=llm, from_start=True)

def format_responses_for_gpt(response: dict[str, object]) -> str:
        '''
        Converts a response dictionary object into a string of questions and answers.
        '''
        answers = response["answers"]
        formatted = list(
            map(
                lambda ans: f'{ans["question_id"]}. {ans["question"]}\n{ans["answer"]}', answers
            )

        )
        return "\n".join(formatted)   


if __name__ == "__main__":
############### TEST HERE ######################
###### This should be moved to test folder #####
    string = """
This survey is for Apple, the software company.
We are conducting a survey for the iphone 69, a new model for the Iphone.


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
    llm = GPT()
    pipe = construct_chatlog(string, llm=llm)
    import re
    for i in range(100):
        output = (llm.run(pipe.message_list))
        print(output)     
        pipe.insert_and_update(output, pipe.current_index, is_llm=True) 

        bye = pipe.message_list.copy()
        bye.append(
            ChatLog.END_QUERY
        )
        result = llm.run(bye)
        if re.search(r"[yY]es", result):
            break

        pipe.insert_and_update(input(), pipe.current_index, is_llm=False)

    print(pipe)
    



   