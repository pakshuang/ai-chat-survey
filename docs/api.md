# API

This document describes the backend API for the project. It is intended to be read by developers and other technical stakeholders. This API contract will allow the frontend team to develop the UI before the backend is complete.

## Admins

Admins are the users who have access to the admin portal. There will be no endpoints to CRUD admins, as they will be created manually in the database. The only way to create an admin is for the engineer to manually insert a record into the database. The admin will then be able to log in and access the admin portal.

### 1. Login

- **Endpoint:** `/admins/login`
- **Method:** `POST`
- **Description:** Log in an admin
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

- **Endpoint:** `/surveys`
- **Method:** `POST`
- **Description:** Create a new survey. An admin JWT is required.
- **Request Body:**

  ```json
  {
    "metadata": {
      "name": "string",
      "description": "string",
      "created_by": "string", # admin username
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
      "status": "string" # draft, published, archived
      "password": "string" # Optional password to protect the survey
    },
    "sections": [
      {
        "title": "string",
        "subtitle": "string",
        "components": [
          {
            "type": "string", # question, text
            "content": "string", # question
            <!-- if type == "question" -->
            "question_id": "integer",
            "question_type": "string", # multiple_choice, short_answer, long_answer, etc.
            "options": ["string"]
          }
        ]
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
  - `500` - Internal Server Error

### 2. Get Surveys

- **Endpoint:** `/surveys/?admin={username}?status={status}`
- **Method:** `GET`
- **Description:** Get all survey objects created by a specific admin. An admin JWT that corresponds to the specified admin's username is required. The status is optional and can be used to filter the surveys by status.
- **Response:**

  ```json
  {
    "surveys": [
      "survey object", # See the response for /surveys/{id} for the structure of a survey object
      "survey object",
      "survey object"
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `500` - Internal Server Error

### 3. Get Survey

- **Endpoint:** `/surveys/{id}`
- **Method:** `GET`
- **Description:** Get a survey object by ID. If the survey is not published, an admin JWT that corresponds to the survey creator is required. Otherwise if the survey is password-protected, an admin JWT or a respondent JWT that has permission to access that survey is required. A published, non-password-protected survey can be accessed by anyone without a JWT.
- **Response:**

  ```json
  {
    "metadata": {
      "id": "integer",
      "name": "string",
      "description": "string",
      "created_by": "string", # admin username
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
      "updated_at": "string", # YYYY-MM-DD HH:MM:SS
      "status": "string" # draft, published, archived

    },
    "sections": [
      {
        "title": "string",
        "subtitle": "string",
        "components": [
          {
            "type": "string", # question, text
            "content": "string", # question
            <!-- if type == "question" -->
            "question_id": "integer",
            "question_type": "string", # mcq, mrq, short_answer, long_answer, etc.
            "options": ["string"] # optional
          }
        ]
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

- **Endpoint:** `/surveys/{id}`
- **Method:** `DELETE`
- **Description:** Delete a survey by ID. An admin JWT that corresponds to the survey creator is required.
- **Response:**

  ```json
  {
    "confirmation": "string"
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `404` - Not Found
  - `500` - Internal Server Error

## Responses

These endpoints are used to submit, read, update, and delete responses, which are the combined data collected from the survey and chat completed by a single respondent.

### 1. Submit Response

- **Endpoint:** `survey/{id}/response`
- **Method:** `POST`
- **Description:** Submit a new response. For a password-protected survey, a respondent JWT is required. For a non-password-protected survey, no JWT is required. The survey must be published. If the submission is successful, a new respondent JWT will be returned in the response body, which can be used to access the chatbot enpoint for this specific response.
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
    "jwt": "string"
  }
  ```

- **Status Codes:**
  - `201` - Created
  - `400` - Bad Request
  - `500` - Internal Server Error

### 2. Get Responses

- **Endpoint:** `/surveys/{id}/response`
- **Method:** `GET`
- **Description:** Get all responses for a survey. An admin JWT that corresponds to the survey creator is required.
- **Response:**

  ```json
  {
    "responses": [
      {
        "response_id": "integer",
        "metadata": {
          "survey_id": "integer",
          "response_id": "integer",
          "submitted_at": "string", # YYYY-MM-DD HH:MM:SS
        },
        "responses": [
          {
            "question_id": "integer",
            "response": "string",
          }
        ]
      }
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `500` - Internal Server Error

### 3. Get Response

- **Endpoint:** `/surveys/{id}/response/{response_id}`
- **Method:** `GET`
- **Description:** Get a response by ID. An admin JWT that corresponds to the survey creator is required.
- **Response:**

  ```json
  {
    "response_id": "integer",
    "metadata": {
      "survey_id": "integer",
      "response_id": "integer",
      "submitted_at": "string", # YYYY-MM-DD HH:MM:SS
    },
    "responses": [
      {
        "question_id": "integer",
        "response": "string",
      }
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `404` - Not Found
  - `500` - Internal Server Error

### 4. Chatbot

- **Endpoint:** `/surveys/{id}/response/{response_id}/chat`
- **Method:** `POST`
- **Description:** Send a message to the chatbot. A respondent JWT that corresponds to the response is required.
- **Request Body:**

  ```json
  {
    "message": "string" # Can be empty since the chatbot will send the first message
  }
  ```

- **Response:**

  ```json
  {
    "message": "string",
    "is_last": "boolean"
  }
  ```

- **Status Codes:**
  - `201` - Created
  - `400` - Bad Request
  - `500` - Internal Server Error

### 5. Login

- **Endpoint:** `/surveys/{id}/login`
- **Method:** `POST`
- **Description:** Log in to a password-protected survey. A respondent JWT will be returned in the response body, which can be used to get the specified survey and submit a response.
- **Request Body:**

  ```json
  {
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
