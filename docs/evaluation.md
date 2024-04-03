# Model Evaluation

Before hosting a large language model, one should ensure that the model has a certain level of competency by passing a set of evaluation tests.

A `model_evaluation` folder has been set up for this purpose, with a template for GPT-4. To run the tests please follow the following instructions.

Before you may begin, you may want to set in the `.env` folder, your HuggingFace api token with

```
HF_API_KEY=
```

```shell
cd ai-chat-survey
docker-compose -f compose.eval.yaml up --build
```

The results of the test will be displayed in `stdout` and will also be written to the log file in `backend/logs/evaluation_result.log`
