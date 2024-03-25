-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS ai_chat_survey_db;

-- Use the created database
USE ai_chat_survey_db;

-- Create the Admins table
CREATE TABLE IF NOT EXISTS Admins (
    admin_username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255),
    created_at TIMESTAMP
);

-- Create the Surveys table
CREATE TABLE IF NOT EXISTS Surveys (
    survey_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    title VARCHAR(255),
    subtitle TEXT,
    admin_username VARCHAR(255),
    created_at TIMESTAMP,
    chat_context TEXT,
    FOREIGN KEY (admin_username) REFERENCES Admins(admin_username)
);

-- Create the Questions table
CREATE TABLE IF NOT EXISTS Questions (
    question_id INT,
    survey_id INT,
    question TEXT,
    question_type VARCHAR(255), -- Consider changing to ENUM once all questions types are decided
    options JSON,
    PRIMARY KEY (question_id, survey_id),
    FOREIGN KEY (survey_id) REFERENCES Surveys(survey_id) ON DELETE CASCADE
);

-- Create the Survey_Responses table
CREATE TABLE IF NOT EXISTS Survey_Responses (
    response_id INT,
    survey_id INT,
    question_id INT,
    answer TEXT,
    submitted_at TIMESTAMP,
    PRIMARY KEY (response_id, question_id, survey_id),
    FOREIGN KEY (survey_id) REFERENCES Surveys(survey_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE
);

-- Create the ChatLog table
CREATE TABLE IF NOT EXISTS ChatLog (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT,
    chat_log JSON,
    created_at TIMESTAMP,
    FOREIGN KEY (survey_id) REFERENCES Surveys(survey_id)
);
