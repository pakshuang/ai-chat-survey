# API

This document describes the backend API for the project. It is intended to be read by developers and other technical stakeholders. This API contract will allow the frontend team to develop the UI before the backend is complete.

## Admins

Admins are the users who have access to the admin portal. There will be no endpoints to RUD admins, but there will be an endpoint to create an admin. The only way to create an admin is for the engineer to manually insert a record into the database. The admin will then be able to log in and access the admin portal.

### 1. Create Admin

- **Endpoint:** `/api/v1/admins`
- **Method:** `POST`
- **Description:** Create a new admin
- **Request Body:**

  ```json
  {
    "username": "string",
    "password": "string",
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
    "password": "string",
  }
  ```

- **Response:**

  ```json
  {
    "jwt": "string"
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `400` - Bad Request
  - `401` - Unauthorized
  - `500` - Internal Server Error

## Surveys

These endpoints are used to create, read, update, and delete surveys, which are the first phase of the survey process.

### 1. Create Survey

- **Endpoint:** `/api/v1/surveys`
- **Method:** `POST`
- **Description:** Create a new survey. A JWT is required.
- **Request Body:**

  ```json
  {
    "metadata": {
      "name": "string",
      "description": "string",
      "created_by": "string", # admin username
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
    },
    "title": "string",
    "subtitle": "string",
    "questions": [
      {
        "id": "integer",
        "type": "string", # multiple_choice, short_answer, long_answer, etc.
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
    "surveys": [
      "survey object", # See the response for /api/v1/surveys/{survey_id} for the structure of a survey object
      "survey object",
      "survey object"
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
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
      "id": "integer",
      "name": "string",
      "description": "string",
      "created_by": "string", # admin username
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
    },
    "title": "string",
    "subtitle": "string",
    "questions": [
      {
        "id": "integer",
        "type": "string", # multiple_choice, short_answer, long_answer, etc.
        "options": ["string"]
      }
    ]
    "chat_context": "string" # The proprietary knowledge that the chatbot needs to have to conduct the chat
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `404` - Not Found
  - `500` - Internal Server Error

### 4. Delete Survey

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

## Responses

These endpoints are used to submit, read, update, and delete responses, which are the combined data collected from the survey and chat completed by a single respondent.

### 1. Submit Response

- **Endpoint:** `/api/v1/survey/{survey_id}/responses`
- **Method:** `POST`
- **Description:** Submit a new response.
- **Request Body:**

  ```json
  {
    "metadata": {
      "survey_id": "integer",
    },
    "responses": [
      {
        "question_id": "integer",
        "response": "string",
      }
    ]
  }
  ```

- **Response:**

  ```json
  {
    "response_id": "integer",
  }
  ```

- **Status Codes:**
  - `201` - Created
  - `400` - Bad Request
  - `404` - Not Found
  - `500` - Internal Server Error

### 2. Get Responses

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses`
- **Method:** `GET`
- **Description:** Get all responses for a survey. An admin JWT that corresponds to the survey creator is required.
- **Response:**

  ```json
  {
    "responses": [
      "response object", # See /api/v1/surveys/{survey_id}/responses/{response_id} for the structure of a response object
      "response object",
      "response object"
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `401` - Unauthorized
  - `403` - Forbidden
  - `404` - Not Found
  - `500` - Internal Server Error

### 3. Get Response

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses/{response_id}`
- **Method:** `GET`
- **Description:** Get a response by ID. An admin JWT that corresponds to the survey creator is required.
- **Response:**

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
        "answer": "string",
      }
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
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

- **Response:**

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
