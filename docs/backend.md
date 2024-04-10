# Backend Report

## Introduction
This section serves as a comprehensive exploration of the backend infrastructure underpinning our AI chatbot survey system. Here, we present an in-depth analysis of the Large Language Model (LLM), in our case ChatGPT, at the heart of our solution, along with a detailed examination of the backend architecture. It aims to provide a thorough understanding of our model selection rationale, its integration into the survey framework, and the overarching architecture supporting its functionality. Furthermore, we discuss our approach to model evaluation, post-deployment tracking, and strategies for continuous improvement.

## Literature Review
- Insert literature review regarding traditional surveys as well as efforts to integrate LLMs into surveys

## Backend Architecture
### 1. Introduction to Backend Architecture

- The backend architecture of our AI Chatbot Survey system serves as the foundation for managing data, handling user interactions, and ensuring system integrity. It plays a pivotal role in supporting the seamless operation of the entire system, from processing user requests to persisting data securely.

- Discussion on how the architecture is designed to handle scalability and ensure optimal performance. Explanation of strategies such as horizontal scaling, caching mechanisms, and load balancing.

### 2. Technology Stack

List of technologies and frameworks used for each component. Justification for the choice of each technology based on factors like scalability, performance, etc.

### 3. Interaction between components
The backend components interact harmoniously to facilitate the flow of data and operations within the system:
- `Frontend` to `Server`: The frontend communicates with the backend server through API endpoints defined in `app.py`, triggering actions such as creating surveys, submitting responses, retrieving data, and sending chat messages.

- `Server` to `Database`: Upon receiving requests, the server interacts with the MySQL database to fetch or store data. SQL queries are executed to perform CRUD operations on tables such as `Surveys`, `Questions`, and `Survey_Responses`, ensuring data persistence and integrity.

- `Authentication/Authorization` Flow: User authentication and authorization processes are handled by the server, which verifies user credentials against the `Admins` table in the database. Upon successful authentication, users are granted access to functionalities based on their assigned roles and permissions.

### 4. Components of the Backend Architecture

#### a. Server/API
The backend server is the core component responsible for processing incoming requests from the frontend via our API, and executing the necessary logic. Implemented using Flask in app.py, the server handles various functionalities such as creating surveys, submitting responses, sending chat messages to ChatGPT, and interacting with the database.

Our API consists of the following:
##### Admins

Admins play a crucial role in managing the system. They have access to an admin portal where they can create and delete surveys, as well as view responses to surveys they create. The API provides endpoints specifically for admin management:

##### 1. Create Admin

- **Endpoint:** `/api/v1/admins`
- **Method:** `POST`
- **Description:** Creates a new admin with a username and password.

##### 2. Login

- **Endpoint:** `/api/v1/admins/login`
- **Method:** `POST`
- **Description:** Logs in an admin and issues a JWT upon successful login.

##### Surveys

Surveys are a fundamental aspect of the AI Chat Bot system, providing the necessary context and structure for interactions. The API supports the creation, retrieval, and deletion of surveys:

##### 1. Create Survey

- **Endpoint:** `/api/v1/surveys`
- **Method:** `POST`
- **Description:** Creates a new survey with metadata, title, subtitle, questions, and chat context.

##### 2. Get Surveys

- **Endpoint:** `/api/v1/surveys/?admin={username}`
- **Method:** `GET`
- **Description:** Retrieves all survey objects, optionally filtered by the admin who created them.

##### 3. Get Survey

- **Endpoint:** `/api/v1/surveys/{survey_id}`
- **Method:** `GET`
- **Description:** Retrieves a survey object by ID.

##### 4. Delete Survey

- **Endpoint:** `/api/v1/surveys/{survey_id}`
- **Method:** `DELETE`
- **Description:** Deletes a survey by ID, requiring admin authentication.

##### Survey Responses

Survey responses capture user interactions and feedback. The API allows for the submission, retrieval, and update of survey responses:

##### 1. Submit Survey Response

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses`
- **Method:** `POST`
- **Description:** Submits a new survey response.
- **Request Body:** JSON format containing response metadata and answers.

##### 2. Get Survey Responses

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses`
- **Method:** `GET`
- **Description:** Retrieves all response objects for a survey, requiring admin authentication.

##### 3. Get Survey Response

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses/{response_id}`
- **Method:** `GET`
- **Description:** Retrieves a response object by ID, requiring admin authentication.

##### 4. Send Chat Message

- **Endpoint:** `/api/v1/surveys/{survey_id}/responses/{response_id}/chat`
- **Method:** `POST`
- **Description:** Sends a message to the chatbot and receives a response.

For the detailed API documentation, refer to [api.md](api.md).

#### b. Database

The MySQL database, named `ai_chat_survey_db`, serves as the centralized repository for storing survey data, user information, chat logs, and other relevant data. It consists of tables including `Admins`, `Surveys`, `Questions`, `Survey_Responses`, and `ChatLog`, designed to efficiently store and manage different types of data.

##### Entity Relationship (ER) Diagram:

![Entity Relationship (ER) Diagram](diagrams/images/db_schema.png)

##### Explanation of [Database Schema](../database/init.sql):

- **Admins**: Stores information about administrators who have access to the system. This table includes fields such as `admin_username`, `password`, and `created_at`.

- **Surveys**: Contains details of the surveys created in the system. Fields include `survey_id`, `title`, `subtitle`, `admin_username`, `created_at`, and `chat_context`.

- **Questions**: Stores the questions associated with each survey. Fields include `question_id`, `survey_id`, `question`, `question_type`, and `options`.

- **Survey_Responses**: Holds the responses submitted for each survey question. Fields include `response_id`, `survey_id`, `question_id`, `answer`, and `submitted_at`.

- **ChatLog**: Logs the chat interactions between users and the chatbot. Fields include `chat_id`, `survey_id`, `response_id`, `chat_log`, and `created_at`.

The database schema is designed to maintain data integrity and efficiently handle various aspects of the AI chatbot survey system, from survey creation to user interactions and response storage.

#### c. Model (ChatGPT)

Tie-back to user interviews conducted by the frontend team to justify the choice of models and solutions in the backend architecture. Explanation of how the architecture aligns with user requirements and expectations gathered from user feedback.

- Add in Model Evaluation
- [Model Evaluation](evaluation.md)
- Rubrics:
    - In-depth study of performance of model and it's failings.
    - Interpretation of model

- Add in Post-Deployment Tracking and Improvement
  - Insert model evaluation
  - Rubrics:
      - Demonstrate an awareness of how model can be tracked and improved after
        deployment.

## Conclusion
In conclusion, this backend report has provided a detailed examination of the infrastructure supporting our AI chatbot survey system. We have explored the core components and discussed the rationale behind using ChatGPT and its integration into the survey framework. Additionally, we have examined the backend architecture, shedding light on the design decisions and the system's functionality.