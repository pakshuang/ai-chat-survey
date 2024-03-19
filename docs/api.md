# API

This document describes the backend API for the project. It is intended to be read by developers and other technical stakeholders. This API contract will allow the frontend team to develop the UI before the backend is complete.

## Admins

These endpoints are used to create, read, update, and delete admins, which are the users who have access to the admin dashboard.

### 1. Create Admin

- **Endpoint:** `/admin`
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
    "confirmation": "string"
  }
  ```

- **Status Codes:**
  - `201` - Created
  - `400` - Bad Request
  - `500` - Internal Server Error

### 2. Get Admins

- **Endpoint:** `/admin/`
- **Method:** `GET`
- **Description:** Get all admin usernames
- **Response:**

  ```json
  {
    "admins": [
      {
        "id": "integer",
        "username": "string"
      }
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `500` - Internal Server Error


### 3. Get Admin

- **Endpoint:** `/admin/{id}`
- **Method:** `GET`
- **Description:** Get an admin by ID
- **Response:**

  ```json
  {
    "id": "integer",
    "username": "string"
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `404` - Not Found
  - `500` - Internal Server Error

### 4. Update Admin

- **Endpoint:** `/admin/{id}`
- **Method:** `PUT`
- **Description:** Update an admin by ID
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
    "confirmation": "string"
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `400` - Bad Request
  - `404` - Not Found
  - `500` - Internal Server Error

### 5. Delete Admin

- **Endpoint:** `/admin/{id}`
- **Method:** `DELETE`
- **Description:** Delete an admin by ID
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

### 6. Login

- **Endpoint:** `/admin/login`
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
    "jwt_token": "string"
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

- **Endpoint:** `/survey`
- **Method:** `POST`
- **Description:** Create a new survey
- **Request Body:**

  ```json
  {
    "metadata": {
      "name": "string",
      "description": "string",
      "created_by": "string", # user ID
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
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

- **Endpoint:** `/survey/`
- **Method:** `GET`
- **Description:** Get all survey objects
- **Response:**

  ```json
  {
    "surveys": [
      "survey object",
      "survey object",
      "survey object"
    ]
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `500` - Internal Server Error

### 3. Get Survey

- **Endpoint:** `/survey/{id}`
- **Method:** `GET`
- **Description:** Get a survey object by ID
- **Response:**

  ```json
  {
    "metadata": {
      "id": "integer",
      "name": "string",
      "description": "string",
      "created_by": "string", # user ID
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
      "updated_by": "string", # user ID
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
            "question_type": "string", # multiple_choice, short_answer, long_answer, etc.
            "options": ["string"]
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

### 4. Update Survey

- **Endpoint:** `/survey/{id}`
- **Method:** `PUT`
- **Description:** Update a survey by ID
- **Request Body:**

  ```json
  {
    "metadata": {
      "id": "string",
      "name": "string",
      "description": "string",
      "created_by": "string", # user ID
      "created_at": "string", # YYYY-MM-DD HH:MM:SS
      "updated_by": "string", # user ID
      "updated_at": "string", # YYYY-MM-DD HH:MM:SS
      "status": "string" # draft, published, archived
    },
    "sections": [
      "section object",
      "section object",
      "section object"
    ],
    "chat_context": "string" # The proprietary knowledge that the chatbot needs to have to conduct the chat
  }
  ```

- **Response:**

  ```json
  {
    "confirmation": "string"
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `400` - Bad Request
  - `404` - Not Found
  - `500` - Internal Server Error

### 5. Delete Survey

- **Endpoint:** `/survey/{id}`
- **Method:** `DELETE`
- **Description:** Delete a survey by ID
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
- **Description:** Submit a new response
- **Request Body:**

  ```json
  {
    "metadata": {
      "survey_id": "integer", # survey ID
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
    "response_id": "integer"
  }
  ```

- **Status Codes:**
  - `201` - Created
  - `400` - Bad Request
  - `500` - Internal Server Error

### 2. Get Responses

- **Endpoint:** `/survey/{id}/response`
- **Method:** `GET`
- **Description:** Get all responses for a survey
- **Response:**

  ```json
  {
    "responses": [
      {
        "response_id": "integer",
        "metadata": {
          "survey_id": "integer", # survey ID
          "response_id": "integer", # user ID
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

- **Endpoint:** `/survey/{id}/response/{response_id}`
- **Method:** `GET`
- **Description:** Get a response by ID
- **Response:**

  ```json
  {
    "response_id": "integer",
    "metadata": {
      "survey_id": "integer", # survey ID
      "response_id": "integer", # user ID
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

### 4. Update Response

- **Endpoint:** `/survey/{id}/response/{response_id}`
- **Method:** `PUT`
- **Description:** Update a response by ID
- **Request Body:**

  ```json
  {
    "metadata": {
      "survey_id": "integer", # survey ID
      "response_id": "integer", # user ID
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
    "confirmation": "string"
  }
  ```

- **Status Codes:**
  - `200` - OK
  - `400` - Bad Request
  - `404` - Not Found
  - `500` - Internal Server Error

### 5. Delete Response

- **Endpoint:** `/survey/{id}/response/{response_id}`
- **Method:** `DELETE`
- **Description:** Delete a response by ID
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

### 6. Chatbot

- **Endpoint:** `/survey/{id}/response/{response_id}/chat`
- **Method:** `POST`
- **Description:** Send a message to the chatbot
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
