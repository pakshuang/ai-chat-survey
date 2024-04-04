# API

This document describes the backend API for the project. It is intended to be read by developers and other technical stakeholders.

## Admins

Admins have access to the admin portal, they can create and delete surveys as well as view the responses to surveys they create. There is an endpoint to Create an admin, but no endpoints to Read, Update, or Delete admins. After creation, the admin is able to log in and access the admin portal.

### 1. Create Admin

- **Endpoint:** `/api/v1/admins`
- **Method:** `POST`
- **Description:** Create a new admin
- **Request Body:**

  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

- **Response:**

  ```json
  {
    "message": "string"
  }
  ```

- **Status Codes:**

  - `201` - Created
  - `400` - Bad Request
  - `500` - Internal Server Error

### 2. Login

- **Endpoint:** `/api/v1/admins/login`
- **Method:** `POST`
- **Description:** Log in an admin. A JWT is issued upon successful login.
- **Request Body:**

  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

- **Response:**

  ```json
  {
    "jwt": "string",
    "jwt_exp": "string" # YYYY-MM-DD HH:MM:SS
  }
  ```

- **Status Codes:**

  - `200` - OK
  - `400` - Bad Request
  - `401` - Unauthorized
  - `500` - Internal Server Error

## Surveys

These endpoints are used to Create, Read, and Delete surveys.

### 1. Create Survey

> [!IMPORTANT]
> A JWT is required.

- **Endpoint:** `/api/v1/surveys`
- **Method:** `POST`
- **Description:** Create a new survey. A JWT is required.
- **Request Body:**

  ```json
  {
    "metadata": {
      "created_by": "string", # admin username
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
    },
    "title": "string",
    "subtitle": "string",
    "questions": [
      {
        "question_id": "integer",
        "type": "string", # multiple_choice, multiple_response, free_response
        "question": "string",
        "options": ["string"]
      }
    ],
    "chat_context": "string" # The proprietary knowledge that the chatbot needs to have to conduct the chat
  }
  ```

- **Response:**

  ```json
  {
    "survey_id": "integer"
  }
  ```

- **Status Codes:**

  - `201` - Created
  - `400` - Bad Request
  - `401` - Unauthorized
  - `500` - Internal Server Error

### 2. Get Surveys

- **Endpoint:** `/api/v1/surveys/?admin={username}`
- **Method:** `GET`
- **Description:** Get all survey objects. An optional query parameter `admin` can be used to filter surveys by the admin who created them.
- **Response:**

  ```json
  {
    [
      "survey object", # See the response for /api/v1/surveys/{survey_id} for the structure of a survey object
      "survey object",
      "survey object"
    ]
  }
  ```

- **Status Codes:**

  - `200` - OK
  - `400` - Bad Request
  - `401` - Unauthorized
  - `403` - Forbidden
  - `500` - Internal Server Error

### 3. Get Survey

- **Endpoint:** `/api/v1/surveys/{survey_id}`
- **Method:** `GET`
- **Description:** Get a survey object by ID.
- **Response:**

  ```json
  {
    "metadata": {
      "survey_id": "integer",
      "created_by": "string", # admin username
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
    },
    "title": "string",
    "subtitle": "string",
    "questions": [
      {
        "question_id": "integer",
        "type": "string", # multiple_choice, multiple_response, free_response
        "question": "string",
        "options": ["string"]
      }
    ],
    "chat_context": "string" # The proprietary knowledge that the chatbot needs to have to conduct the chat
  }
  ```

- **Status Codes:**

  - `200` - OK
  - `404` - Not Found
  - `500` - Internal Server Error

### 4. Delete Survey

> [!IMPORTANT]
> A JWT is required.

- **Endpoint:** `/api/v1/surveys/{survey_id}`
- **Method:** `DELETE`
- **Description:** Delete a survey by ID. An admin JWT that corresponds to the survey creator is required.
- **Response:**

  ```json
  {
    "message": "string"
  }
  ```

- **Status Codes:**

  - `200` - OK
  - `400` - Bad Request
  - `401` - Unauthorized
  - `403` - Forbidden
  - `404` - Not Found
  - `500` - Internal Server Error

## Survey Responses

> [!NOTE]
> Survey responses (reponse objects) are json objects, representing a respondents answers to a survey as well as their chatlog. HTTP responses are also json objects, but they are the entire response from the API. The two are different and should not be confused.

These endpoints are used to Create, Read, and Update (send message) responses, which are the combined data collected from the answers and chat completed by a single respondent.

### 1. Submit Survey Response

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses`
- **Method:** `POST`
- **Description:** Submit a new survey response (response object).
- **Request Body:**

  ```json
  {
    "metadata": {
      "survey_id": "integer"
    },
    "answers": [
      {
        "question_id": "integer",
        "type": "string", # multiple_choice, multiple_response, free_response
        "question": "string",
        "options": ["string"],
        "answer": ["string"],
      }
    ]
  }
  ```

- **HTTP Response:**

  ```json
  {
    "response_id": "integer" # survey response id
  }
  ```

- **Status Codes:**

  - `201` - Created
  - `400` - Bad Request
  - `404` - Not Found
  - `500` - Internal Server Error

### 2. Get Survey Responses

> [!IMPORTANT]
> A JWT is required.

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses`
- **Method:** `GET`
- **Description:** Get all response objects for a survey. An admin JWT that corresponds to the survey creator is required.

- **HTTP Response:**

  ```json
  {
    [
      "response object", # See /api/v1/surveys/{survey_id}/responses/{response_id} for the structure of a response object
      "response object",
      "response object"
    ]
  }
  ```

- **Status Codes:**

  - `200` - OK
  - `400` - Bad Request
  - `401` - Unauthorized
  - `403` - Forbidden
  - `404` - Not Found
  - `500` - Internal Server Error

### 3. Get Survey Response

> [!IMPORTANT]
> A JWT is required.

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses/{response_id}`
- **Method:** `GET`
- **Description:** Get a response object by ID. An admin JWT that corresponds to the survey creator is required.
- **HTTP Response:**

  ```json
  {
    "metadata": {
      "survey_id": "integer",
      "response_id": "integer",
      "submitted_at": "string", # YYYY-MM-DD HH:MM:SS
    },
    "answers": [
      {
        "question_id": "integer",
        "type": "string", # multiple_choice, multiple_response, free_response
        "question": "string",
        "options": ["string"],
        "answer": ["string"],
      }
    ]
  }
  ```

- **Status Codes:**

  - `200` - OK
  - `400` - Bad Request
  - `401` - Unauthorized
  - `403` - Forbidden
  - `404` - Not Found
  - `500` - Internal Server Error

### 4. Send Chat Message

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses/{response_id}/chat`
- **Method:** `POST`
- **Description:** Send a message to the chatbot. The chatbot will respond with a message.
- **Request Body:**

  ```json
  {
    "content": "string" # Can be an empty string since the chatbot will send the first message
  }
  ```

- **HTTP Response:**

  ```json
  {
    "content": "string",
    "is_last": "boolean" # Whether this is the last message that the chatbot will send
  }
  ```

- **Status Codes:**

  - `201` - Created
  - `400` - Bad Request
  - `404` - Not Found
  - `500` - Internal Server Error
