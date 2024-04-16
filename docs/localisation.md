# Localisation
This script is only meant for technical stakeholders committed to the localisation of the LLM in this project. It provides some assistance and groundwork for what could be done in the future for this app.

## Motivation

In the modern data-centric environment, companies prioritize safeguarding sensitive information while enhancing operational efficiency. To achieve these goals, leveraging Local Language Models (LLMs) becomes crucial.

While LLMs are accessible via APIs, relying solely on external services can pose risks, especially if these APIs cease to provide LLM support, causing disruptions.

Furthermore, maintaining data privacy is paramount for companies, making it essential to avoid sharing sensitive information with external API providers when interacting with a model. Deploying LLMs internally helps mitigate these risks and ensures data remains secure within the organization's infrastructure.

## Suggestions

An existing script `root/scripts/finetuning/GPTQLoRA-script.py` has been created to provide a simple pipeline for future finetuning efforts. To run this script, one needs to have a different set of Python dependencies from the rest of the app, which primarily focuses on the deployment of the Large Language Model.

> **Warning**: Pipenv does not seem to be compatible with Pytorch for GPU support. We recommend using another python environment.

## Requirements
1. Nvidia GPU with a bare minimum of 8GB VRAM, and a soft requirement of 16GB VRAM.
2. Python 3.11.8
3. CUDA 11.8 and above. You may check this by running `nvcc -V` in the CLI.

## Installation

1. Simply install from `requirements.txt` normally, or within an environment of your choice. After activating your desired environment,
```shell
pip install -r requirements.txt
```
2. (Optional) Ideally, one would like a local copy of a GPTQ base model. The following is an example of how to obtain such a model in the `models` folder:
```shell
cd ai-chat-survey/backend-gpu/models
git clone git clone https://huggingface.co/TheBloke/Nous-Hermes-2-SOLAR-10.7B-GPTQ -b gptq-4bit-32g-actorder_True
```

## Finetuning

The script is to be run from the CLI, with arguments. This script finetunes a GPTQ-quantised model with parameter-efficient finetuning techniques to reduce computational time and memory. This is done with a LORA adapter. After training, the LORA model will be saved in `backend-gpu/models/`, where ideally, one could deploy the app in a container.

The reasoning behind using GPTQ quantised LLMs instead of other quantisation methods like AWQ or GGUF is due to the widespread availability of GPTQ models on HuggingFace, as well as GPTQ models to be run quickly on a GPU, which is compulsory for a web app with a minimal amount of traffic.

**Warning**: The current app, and therefore the backend container, for demonstration purposes, currently uses a closed-source model. The necessary installations and libraries needed to run an open-source model locally are omitted due to the long installation times required. The current backend container does **NOT** have access to the GPU.

The finetuning script is intended to be run from the CLI using several available arguments.

### **Required** Arguments

`--base`- Base model (huggingface name or path to GPTQ folder) to finetune. For example, "TheBloke/dolphin-2.2.1-mistral-7B-GPTQ" is a repository on huggingface. Supplying this to the argument will automatically download and load a model (from the `main` branch). This argument is supplied into the `AutoModelForCausalLM.from_pretrained` method.

`--dataset-path` - Path to a dataset, in `csv` format. The dataset MUST have an `input` column, an `output` column and optionally, a `system` column, for the system prompt. It is recommended to include the system prompt.

`--bits` - Number of bits to quantise. Supplied to the [GPTQConfig](https://huggingface.co/docs/transformers/main_classes/quantization#transformers.GPTQConfig) class.

### Optional Arguments

`--output-path` - Output directory of the trained adapter model. Defaults to the `models` folder.
`--learning-rate` - Learning rate of the model. Defaults to `2.5e-4`.
`--steps` - Total number of training steps. Defaults to `256`
`--r` - Rank hyperparameter of the LORA. Defaults to `16`.
`--lora-alpha` - Alpha hyperparameter. Defaults to `16`.
`--lora-dropout` - Dropout value for the LORA. Defaults to `0.05`
`--train-size` - Proportion of training data in the dataset. Note that validation and test data are split evenly among the remaining data.
`--seed` - Used when splitting the dataset into train-test-validation before training. **NOT** used for model generation. Set to -1 for randomisation by default.
`--has-system-prompt` - To accomodate pretrained models like Mistral with no system prompt and are instead trained on Instruction-Output pairs.
`--max-len` - Max length of tokens supplied to finetune the model. Also doubles as a max generation length in the second portion of the file.
`--batch_size` - The batch size **per GPU** for training. Defaults to 4.

### Example
```shell
python GPTQLoRA-script.py --base ../../backend-gpu/models/dolphin-2.2.1-mistral-7B-GPTQ --dataset-path C:\Users\ME\Downloads\datee.csv --output-path ../../backend-gpu/models --has-system-prompt 0 --train-size 0.5 --r 8 --bits 4 --steps 100
```
Explanation:
The following command assumes one has downloaded a model from huggingface and provides it to base. The Mistral models have not been trained with system prompts, so `datee.csv` is a `csv` file with `input` and `output` columns containing expected queries and responses to the LLM, and there is no need for a `system` column. `--has-system-prompt` is, for the same reason, set to 0. The output path of the trained adapter model is set to the `models` folder, but this is already done by default.


## Deployment

> **Warning**
> You are reminded that localisation is beyond the scope of this project. This portion only serves as a proof of concept.
> A Nvidia GPU with >=8GB of VRAM is COMPULSORY, and a GPU with >=16GB of VRAM is STRONGLY RECOMMENDED.

A new docker container has been set up to run for local models. This container is run from the image `backend-gpu`. This docker container has:
 - Access to the GPU
 - Pytorch and other dependencies listed in `Pipfile and Pipfile.lock`
 - A `models` folder, which contains localised LLMs in GPTQ format.

The class `LocalMistralGPTQ` is defined in src/llm_classes/llm_level.py. This is a wrapper class for the GPTQ quantised LLM dolphin-2.2.1-mistral-7B-GPTQ. To download the model, simply do the following:

```shell
cd backend-gpu/models
git clone https://huggingface.co/TheBloke/dolphin-2.2.1-mistral-7B-GPTQ -b gptq-4bit-32g-actorder_True
```

Once the model is downloaded, you may run the app with the model with the following command:
> **Warning**
> Do NOT expect results as good as GPT-4. GPT-4 contains around 250 times the number of parameters!
> You may encounter an error generating a response. This is due to a timeout error. Consider using a faster GPU.
> You may even require multiple GPUs.

```shell
docker compose -f compose.yaml -f compose.gpu.yaml up --build
```

The class `LocalMistralPEFTGPTQ` has also been defined. This class represents a finetuned Mistral-7b-GPTQ model. To run the app using this model, you will need to redefine the variables in `app.py`.