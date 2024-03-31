-- Use the created database
USE ai_chat_survey_db;
-- Insert data into the Admins table
INSERT INTO Admins (admin_username, password, created_at)
VALUES (
        'dummyadmin',
        'dummypassword',
        NOW()
    );
    -- Insert data into the Surveys table
INSERT INTO Surveys (
        title,
        subtitle,
        admin_username,
        created_at,
        chat_context
    )
VALUES (
        'P&G Environmentally Friendly Laundry Detergents',
        'This product is designed to cater to environmentally conscious consumers who are looking for effective cleaning solutions that are also gentle on the planet. The detergent is formulated using biodegradable ingredients and comes in a fully recyclable packaging. The goal of this market research is to gather feedback on consumer preferences and concerns regarding environmentally friendly laundry products, which will help in fine-tuning the product and marketing strategies.',
        'dummyadmin',
        NOW(),
        'At Procter & Gamble, we are excited to introduce our latest innovation in household cleaning products: an environmentally friendly laundry detergent. Understanding the growing concern for sustainable and effective cleaning solutions, this new product combines the efficiency and reliability of P&G''s detergents with a strong commitment to environmental stewardship. Formulated with biodegradable ingredients, the detergent ensures a powerful clean while being gentle on the earth. The packaging, made from fully recyclable materials, reflects our dedication to reducing plastic waste. This market research is aimed at understanding consumer preferences in eco-friendly laundry products, their expectations in terms of efficacy, scent, and price, and their overall perception of sustainable products. The insights gained will be invaluable in ensuring that our new detergent not only meets but exceeds the needs and expectations of environmentally conscious consumers.'
    );
-- Insert data into the Questions table
INSERT INTO Questions (
        question_id,
        survey_id,
        question,
        question_type,
        options
    )
VALUES (
        1,
        1,
        'How important is environmental sustainability to you when purchasing laundry detergent?',
        'multiple_choice',
        '["Not at all important", "Slightly Important", "Important", "Fairly Important", "Very Important"]'
    ),
    (
        2,
        1,
        'What key features do you look for in a laundry detergent? (Select all that apply)',
        'multiple_response',
        '["Ingredient transparency", "Sustainable packaging", "Affordability", "Brand reputation", "Effectiveness", "Other"]'
    ),
    (
        3,
        1,
        'Have you used environmentally friendly laundry detergents before?',
        'multiple_choice',
        '["Yes", "No"]'
    ),
    (
        4,
        1,
        'What price range do you consider reasonable for an eco-friendly laundry detergent?',
        'free_response',
        NULL
    ),
    (
        5,
        1,
        'In your own words, what are some characteristics or features of a laundry detergent that make it eco-friendly?',
        'free_response',
        NULL
    ),
    (
        6,
        1,
        'How would you rate P&G''s commitment to environmental sustainability?',
        'multiple_choice',
        '["Not at all committed", "Slightly committed", "Moderately committed", "Very much committed", "Extremely committed"]'
    );
-- Insert data into the Survey_Responses table
INSERT INTO Survey_Responses (
        response_id,
        survey_id,
        question_id,
        answer,
        submitted_at
    )
VALUES (
        1,
        1,
        1,
        '["Slightly Important"]',
        NOW()
    ),   
    (
        1,
        1,
        2,
        '["Affordability", "Effectiveness", "Brand reputation"]',
        NOW()
    ),
    (
        1,
        1,
        3,
        '["Yes"]',
        NOW()
    ),
    (
        1,
        1,
        4,
        '["< $3 per 5 litres"]',
        NOW()
    ),
    (
        1,
        1,
        5,
        '["No microplastics, biodegradable ingredients, recyclable packaging"]',
        NOW()
    ),
    (
        1,
        1,
        6,
        '["Very much committed"]',
        NOW()
    ),
    (
        2,
        1,
        1,
        '["Very Important"]',
        NOW()
    ),
    (
        2,
        1,
        2,
        '["Ingredient transparency", "Other"]',
        NOW()
    ),
    (
        2,
        1,
        3,
        '["Yes"]',
        NOW()
    ),
    (
        2,
        1,
        4,
        '["Around $10 for a bag of 20 pods"]',
        NOW()
    ),
    (
        2,
        1,
        5,
        '["Phosphate-free, high-efficiency formula, cruelty-free"]',
        NOW()
    ),
    (
        2,
        1,
        6,
        '["Slightly committed"]',
        NOW()
    );
-- Insert data into the ChatLog table
INSERT INTO ChatLog (survey_id, response_id, chat_log, created_at)
VALUES (
        1,
        1,
        '{"messages": [{"sender": "client", "message": "User message 1", "timestamp": "2024-03-23 10:00:00"}, {"sender": "bot", "message": "Bot response 1", "timestamp": "2024-03-23 10:05:00"}, {"sender": "client", "message": "User message 2", "timestamp": "2024-03-23 10:10:00"}, {"sender": "bot", "message": "Bot response 2", "timestamp": "2024-03-23 10:15:00"}]}',
        NOW()
    );