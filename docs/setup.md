# Setup

This document describes how to set up the project for development. It is intended to be read by developers and other technical stakeholders.

## Prerequisites

- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)

## Installation

1. Clone the repository:

    ```shell
    git clone
    ```

2. Change into the project directory:

    ```shell
    cd ai-chat-survey
    ```

3. Initialise `.env` file:

    ```shell
    cp sample.env .env
    ```

## Running the Application

To run the application, use the following command:

```shell
docker-compose up --build
```

If you have already built the images, you can use the following command to start the application:

```shell
docker-compose up
```

## Development

### Setting up the development environment

1. Install [pipenv](https://pypi.org/project/pipenv/):

    ```shell
    pip install pipenv
    ```

2. Navigate to either the `frontend` or `backend` directory (depending on which part of the application you are working on):

    ```shell
    cd frontend
    ```

    or

    ```shell
    cd backend
    ```

3. Install the dependencies:

    ```shell
    pipenv install --dev
    ```

4. Adding dependencies:

    If you need to add a new dependency, use the following command:

    ```shell
    pipenv install <package-name>
    ```

    - You can specify if the package is a development dependency by adding the `--dev` flag.
    - Remember to commit the `Pipfile` and `Pipfile.lock` after adding a new dependency.
    - Make sure you install the dependencies in the correct `Pipfile` (frontend or backend).

5. For more information on how to use `pipenv`, refer to the [official documentation](https://pipenv.pypa.io/en/latest/).

### Running a component (pipenv)

Navigate to either the `frontend` or `backend` directory (depending on which part of the application you are working on):

```shell
cd frontend
```

or

```shell
cd backend
```

#### Frontend

```shell
pipenv run streamlit run src/streamlit_app.py
```

or if you use VS Code and have selected the pipenv environment as your interpreter:

```shell
streamlit run src/streamlit_app.py
```

#### Backend

```shell
pipenv run python src/app.py
```

or if you use VS Code and have selected the pipenv environment as your interpreter:

```shell
python src/app.py
```

### Running a component (Docker)

#### Building the images

##### Frontend

```shell
docker build -t frontend .
```

##### Backend

```shell
docker build -t backend .
```

#### Running the images

```shell
docker run --name frontend -p 8501:8501 --env-file ../.env frontend 
```

```shell
docker run --name backend -p 5000:5000 --env-file ../.env backend
```

Note that the network configuration is not set up in the above commands. Running both containers this way will not allow them to communicate with each other. To set up the network configuration, see [Running the Application](#running-the-application).

## Testing

TODO: Add testing instructions once the testing framework is set up.
