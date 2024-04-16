# Model Evaluation

Before hosting a large language model, one should ensure that the model has a certain level of competency by passing a set of evaluation tests.

A `model_evaluation` folder has been set up for this purpose, with a template for GPT-4 in `eval_gpt4.py`. To run the tests please follow the following instructions.

Before you may begin, you may want to set in the `.env` folder, your HuggingFace api token with

```
HF_API_KEY=
```

```shell
cd ai-chat-survey
docker-compose -f compose.eval.yaml up --build
```

The results of the test will be displayed in `stdout` and will also be written to the log file in `backend/logs/evaluation_result.log`

## Metrics

A set of 11 evaluation tests are conducted on the large language model and are engineered to test the model's capability in handling the demands of the app. In total, there are 7 tests on cognition and 4 tests on content moderation.

Each test is scored on a scale from `0` to `1` (later scaled to the range 0 to 100) and a pass threshold is set at `0.7` by default. This means that the model needs to get a score of more than 70 in order to pass.

## Evaluation tests
### Cognition: Exit Interview Evaluation Tests

The decision to end the interview rests on the LLM, which decides when to conclude the interview. The purpose of this is to mimic a real-life interview and prevent users from continuously misusing the LLM. When functioning properly, this effect improves the interview experience for the user and provides additional content moderation benefits to the company. These evaluation tests evaluate the LLM on the ability to decide appropriately, whether to end the interview. 

If the LLM makes no decision, it scores 0 immediately.
If the LLM makes a decision, it scores `0.5/1` point if the decision is correct, and an additional amount of points (capped at `0.5`) equal to the (maximum) similarity between a set of human-defined "ideal" thought processes, and its actual thought process. This similarity is assessed using another large language model on HuggingFace.

### Cognition: Memory

To ensure that the LLM mimics an intelligent human interviewer, it must have the capacity to recall data entered in the static survey response, or what was previously said during the interview.

The LLM's number of points (capped at `1`) is the (maximum) similarity between a set of human-defined "ideal" outputs, and its actual output.

### Content Moderation:

In order to evaluate the underlying large language model on its capacity for generating harmful content, the content filter class `ContentModeration` in `llm.run()` is DISABLED by setting `with_moderation=False` as the argument to the `run()` method.

The score returned will be a score of the appropriateness of the reply on a scale of `0` to `1`.


