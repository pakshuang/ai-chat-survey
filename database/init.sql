-- Create a new database if it doesn't exist
CREATE DATABASE IF NOT EXISTS ai_chat_survey_db;

-- Use the newly created database
USE ai_chat_survey_db;

-- Dummy table named 'users' for testing
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Insert some dummy data into the 'users' table for testing
INSERT INTO users (username, email) VALUES
    ('john_doe', 'john@example.com'),
    ('jane_smith', 'jane@example.com'),
    ('mike_jackson', 'mike@example.com');
