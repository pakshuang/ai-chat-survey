-- Use the created database
USE ai_chat_survey_db;

-- Insert data into the Admins table
INSERT INTO Admins (admin_username, password, created_at)
VALUES
    ('admin1', 'password1', NOW()),
    ('admin2', 'password2', NOW());

-- Insert data into the Surveys table
INSERT INTO Surveys (name, description, title, subtitle, admin_username, created_at)
VALUES
    ('Survey 1', 'Description of Survey 1', 'Title of Survey 1', 'Subtitle of Survey 1', 'admin1', NOW()),
    ('Survey 2', 'Description of Survey 2', 'Title of Survey 2', 'Subtitle of Survey 2', 'admin2', NOW());

-- Insert data into the Questions table
INSERT INTO Questions (survey_id, question, question_type, options)
VALUES
    (1, 'What is your favorite color?', 'Multiple Choice', '{"options": ["Red", "Blue", "Green"]}'),
    (1, 'How old are you?', 'Open-ended', NULL),
    (2, 'Which of the following sports do you like?', 'Multiple Choice', '{"options": ["Football", "Basketball", "Tennis", "Swimming"]}');

-- Insert data into the Survey_Responses table
INSERT INTO Survey_Responses (survey_id, response, submitted_at)
VALUES
    (1, 'Blue', NOW()),
    (1, '25', NOW()),
    (2, 'Football, Tennis', NOW());

-- Insert data into the ChatLog table
INSERT INTO ChatLog (survey_id, chat_log, created_at)
VALUES
    (1, '{"messages": [{"sender": "client", "message": "User message 1", "timestamp": "2024-03-23 10:00:00"}, {"sender": "bot", "message": "Bot response 1", "timestamp": "2024-03-23 10:05:00"}, {"sender": "client", "message": "User message 2", "timestamp": "2024-03-23 10:10:00"}, {"sender": "bot", "message": "Bot response 2", "timestamp": "2024-03-23 10:15:00"}]}', NOW()),
    (2, '{"messages": [{"sender": "client", "message": "User message 1", "timestamp": "2024-03-23 11:00:00"}, {"sender": "bot", "message": "Bot response 1", "timestamp": "2024-03-23 11:05:00"}, {"sender": "client", "message": "User message 2", "timestamp": "2024-03-23 11:10:00"}, {"sender": "bot", "message": "Bot response 2", "timestamp": "2024-03-23 11:15:00"}]}', NOW());