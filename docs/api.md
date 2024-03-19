# API

This document describes the backend API for the project. It is intended to be read by developers and other technical stakeholders. This API contract will allow the frontend team to develop the UI before the backend is complete.

## Admins

These endpoints are used to create, read, update, and delete admins, which are the users who have access to the admin dashboard.




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
            "type": "question",
            "question_type": "string",
            "question": "string",
            "options": ["string"]
          },
          {
            "type": "text",
            "content": "string"
          }
        ]
      }
    ],
    "interview_context": "string" # The proprietary knowledge that the interviewer needs to have to conduct the interview
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
    "interview_context": "string" # The proprietary knowledge that the interviewer needs to have to conduct the interview
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
    "interview_context": "string" # The proprietary knowledge that the interviewer needs to have to conduct the interview
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

## Interviews

These endpoints are used to facilitate interviews, which are the second phase of the survey process.

TODO: Add interview endpoints

## Responses

These endpoints are used to submit, read, update, and delete responses, which are the combined data collected from the survey and interview completed by a single respondent.

### 1. Submit Response

- **Endpoint:** `/response`
- **Method:** `POST`
- **Description:** Submit a new response
