# Backend Report

## Section Introduction
This section serves as a comprehensive exploration of the backend infrastructure underpinning our AI chatbot survey system. Here, we present an in-depth analysis of the LLM (Large Language Model) at the heart of our solution, along with a detailed examination of the backend architecture. Through this report, we aim to provide a thorough understanding of our model selection rationale, its integration into the survey framework, and the overarching architecture supporting its functionality. Furthermore, we discuss our approach to model evaluation, post-deployment tracking, and strategies for continuous improvement.

## Literature Review
- Insert literature review regarding traditional surveys as well as efforts to 
integrate LLMs into surveys

## Backend Architecture
### 1. Introduction to Backend Architecture

The backend architecture of our AI Chatbot Survey system serves as the foundation for managing data, handling user interactions, and ensuring system integrity. It plays a pivotal role in supporting the seamless operation of the entire system, from processing user requests to persisting data securely.

### 2. Components of the Backend Architecture

#### a. Server

The backend server is the core component responsible for processing incoming requests from the frontend and executing the necessary logic. Implemented using Flask in app.py, the server handles various functionalities such as creating surveys, submitting responses, sending chat messages to ChatGPT, and interacting with the database.

#### b. Database

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


#### c. API

The API provides a standardized interface through which the frontend communicates with the backend. Documented in [API](api.md), it defines endpoints for various operations such as creating surveys, submitting responses, retrieving data, and sending chat messages. This facilitates seamless interaction between the frontend and backend components.

#### d. Authentication/Authorization

Authentication and authorization components ensure secure access to the system. The Admins table stores admin credentials, and mechanisms are implemented in the backend to authenticate users and authorize access to restricted functionalities based on their roles and permissions. This safeguards the system from unauthorized access and maintains data security.

### e. Interactions between Components
The backend components interact harmoniously to facilitate the flow of data and operations within the system:
- Frontend to Server: The frontend communicates with the backend server through API endpoints defined in app.py, triggering actions such as creating surveys, submitting responses, retrieving data, and sending chat messages.

- Server to Database: Upon receiving requests, the server interacts with the MySQL database to fetch or store data. SQL queries are executed to perform CRUD operations on tables such as Surveys, Questions, and Survey_Responses, ensuring data persistence and integrity.

- Authentication/Authorization Flow: User authentication and authorization processes are handled by the server, which verifies user credentials against the Admins table in the database. Upon successful authentication, users are granted access to functionalities based on their assigned roles and permissions.

- Data Flow: Data flows between various tables in the database as surveys are created, questions are added, responses are submitted, chat logs are recorded, and user messages are processed by ChatGPT. Foreign key constraints maintain referential integrity, ensuring data consistency and reliability.
### 4. Technology Stack

List of technologies and frameworks used for each component. Justification for the choice of each technology based on factors like scalability, performance, etc.

### 5. Scalability and Performance Considerations

Discussion on how the architecture is designed to handle scalability and ensure optimal performance. Explanation of strategies such as horizontal scaling, caching mechanisms, and load balancing.

### 6. Justification for Models/Solution Chosen

Tie-back to user interviews conducted by the frontend team to justify the choice of models and solutions in the backend architecture. Explanation of how the architecture aligns with user requirements and expectations gathered from user feedback.
  
## Model Evaluation
- [Model Evaluation](evaluation.md)
- Rubrics: 
  - In-depth study of performance of model and it's failings.
  - Interpretation of model

## Post-Deployment Tracking and Improvement
- Insert model evaluation
- Rubrics:
   - Demonstrate an awareness of how model can be tracked and improved after
     deployment.

## Conclusion
In conclusion, this backend report has provided a detailed examination of the infrastructure supporting our AI chatbot survey system. We have explored the core components, including the LLM model, and discussed the rationale behind our model selection and its integration into the survey framework. Additionally, we have examined the backend architecture, shedding light on the design decisions and the system's functionality. Through thorough model evaluation and post-deployment tracking, we have gained insights into the performance of our solution and identified avenues for improvement. 
