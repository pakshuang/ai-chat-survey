# Backend Report

## Introduction

This section serves as a comprehensive exploration of the backend infrastructure underpinning our AI chatbot survey system. Here, we present an in-depth analysis of the Large Language Model (LLM), in our case ChatGPT, at the heart of our solution, along with a detailed examination of the backend architecture. It aims to provide a thorough understanding of our model selection rationale, its integration into the survey framework, and the overarching architecture supporting its functionality. Furthermore, we discuss our approach to model evaluation, post-deployment tracking, and strategies for continuous improvement.

## Literature Review

- Insert literature review regarding traditional surveys as well as efforts to integrate LLMs into surveys

## Backend Architecture

### 1. Introduction to the Backend Architecture

![Backend Architecture](diagrams/images/backend-architecture.png)

- The backend architecture of our AI Chatbot Survey system serves as the foundation for managing data, handling respondent interactions, and ensuring system integrity. It plays a pivotal role in supporting the seamless operation of the entire system, from processing respondent requests to persisting data securely.

- The backend is composed of three key components: the `API`, the `Database`, and the `Model`.
  - **API**: The API component acts as the intermediary between the frontend and the backend. It receives requests from the frontend, processes them, and interacts with the database to fetch or store data. It also conducts prompt engineering and communicates with the model for chatbot interactions.
  - **Database**: The database component stores and manages the system's data, including surveys, responses, chat logs, and admin information. It ensures data integrity, persistence, and efficient retrieval.
  - **Model**: The model component, GPT-4, serves as the conversational agent for the chatbot. It generates responses to respondent messages, providing a conversational interface for survey interactions. The model is integrated into the system through the OpenAI API, enabling real-time chatbot interactions.

### 2. Technology Stack

- **API (Flask)**: Flask was chosen for the API component due to its lightweight nature, simplicity, and flexibility. Flask is well-suited for building RESTful APIs, making it an ideal choice for our system's backend. It provides a robust framework for handling HTTP requests, routing, and interacting with the database.
- **Database (MySQL)**: MySQL was selected as the database management system for its reliability, scalability, and performance. MySQL is a widely-used relational database that offers ACID compliance, data security, and efficient data retrieval. It provides robust support for complex queries, transactions, and data integrity.
- **Model (ChatGPT)**: GPT-4 was chosen as the conversational model for the chatbot component. ChatGPT offers state-of-the-art conversational capabilities, enabling natural and engaging interactions with respondents. It leverages the power of large language models to generate contextually relevant responses, enhancing the respondent experience.
- **Authentication (JWT)**: JSON Web Tokens (JWT) are used for admin authentication and authorization in the system. JWT provides a secure and efficient way to verify admin identities and manage access control. It enables the API to authenticate admins, issue tokens, and enforce role-based access policies.
- **Testing (Pytest, Unittest)**: Pytest and Unittest are utilized for testing the backend components, ensuring code quality, reliability, and functionality. Pytest offers a powerful testing framework with support for fixtures, parametrization, and test discovery. Unittest provides a built-in testing framework for writing test cases and asserting expected outcomes.
- **Formatting (Black, isort)**: Black and isort are used for code formatting and style consistency. Black automatically formats Python code to adhere to PEP 8 guidelines, enhancing readability and maintainability. Isort sorts import statements alphabetically, making code organization more structured and uniform.

### 3. Interaction between components

The backend components interact harmoniously to facilitate the flow of data and operations within the system:

- `Client` to `API Controller Layer` through `Reverse Proxy`: The client sends HTTP requests to the `API Controller Layer` via a reverse proxy, which forwards requests to the appropriate endpoints. The `API Controller Layer` processes incoming requests, performs authentication if required using JWTs, and interacts with the `Service Logic Layer` to fulfill the requests.

- `Service Logic Layer` to `Data Access Layer`: Upon receiving requests, the `Service Logic Layer` applies the business logic and accesses the `Data Access Layer` to access or modify data in the database.

- `Data Access Layer` to `Database`: The `Data Access Layer` interacts with the `Database` to perform CRUD operations, ensuring data integrity and persistence.

- `Service Logic Layer` to `Prompt Engineering Layer`: In the case of chatbot interactions, the `Service Logic Layer` communicates with the `Prompt Engineering Layer` to generate prompts for the model based on respondent answers and messages. The `Prompt Engineering Layer` is responsible for guiding the model's responses and ensuring contextually relevant interactions.

- `Prompt Engineering Layer` to `OpenAI API Integration Layer`: The `Prompt Engineering Layer` interfaces with the `OpenAI API Integration Layer` to send prompts to the GPT-4 model and receive responses. The `OpenAI API Integration Layer` manages the communication with the OpenAI API, handling model interactions and responses.

- `API Controller Layer` to `Client`: The `API Controller Layer` sends HTTP responses back to the client, providing the requested data, acknowledging the completion of operations, or forwarding chatbot responses generated by the model.

### 4. Components of the Backend Architecture

#### a. Server/API

The backend server is the core component responsible for processing incoming requests from the frontend via our API, and executing the necessary logic. Implemented using Flask in app.py, the server handles various functionalities such as creating surveys, submitting responses, sending chat messages to ChatGPT, and interacting with the database.

Our API consists of the following:
<style scoped>
table {
  font-size: 10px;
}
</style>

| Resource: API Method                     | Endpoint                                                   | HTTP Method | Description                                                                       |
|-----------------------------------------|------------------------------------------------------------|--------|-----------------------------------------------------------------------------------|
| **Admins: Create Admin**                | `/api/v1/admins`                                           | POST   | Creates a new admin with a username and password.                                 |
| **Admins: Login**                       | `/api/v1/admins/login`                                     | POST   | Logs in an admin and issues a JWT upon successful login.                          |
| **Surveys: Create Survey**              | `/api/v1/surveys`                                          | POST   | Creates a new survey with metadata, title, subtitle, questions, and chat context. |
| **Surveys: Get Surveys**                | `/api/v1/surveys/?admin={username}`                        | GET    | Retrieves all survey objects, optionally filtered by the admin who created them.  |
| **Surveys: Get Survey**                 | `/api/v1/surveys/{survey_id}`                              | GET    | Retrieves a survey object by ID.                                                  |
| **Surveys: Delete Survey**              | `/api/v1/surveys/{survey_id}`                              | DELETE | Deletes a survey by ID, requiring admin authentication.                           |
| **Survey Responses: Submit Response**   | `/api/v1/surveys/{survey_id}/responses`                    | POST   | Submits a new survey response.                                                    |
| **Survey Responses: Get Responses**     | `/api/v1/surveys/{survey_id}/responses`                    | GET    | Retrieves all response objects for a survey, requiring admin authentication.      |
| **Survey Responses: Get Response**      | `/api/v1/surveys/{survey_id}/responses/{response_id}`      | GET    | Retrieves a response object by ID, requiring admin authentication.                |
| **Survey Responses: Send Chat Message** | `/api/v1/surveys/{survey_id}/responses/{response_id}/chat` | POST   | Sends a message to the chatbot and receives a response.                           |

For the detailed API documentation, refer to [api.md](api.md).

#### b. Database

The MySQL database, named `ai_chat_survey_db`, serves as the centralized repository for storing survey data, user information, chat logs, and other relevant data. It consists of tables including `Admins`, `Surveys`, `Questions`, `Survey_Responses`, and `ChatLog`, designed to efficiently store and manage different types of data.

##### Entity Relationship (ER) Diagram

![Entity Relationship (ER) Diagram](diagrams/images/db_schema.png)

##### Explanation of [Database Schema](../database/init.sql)

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
