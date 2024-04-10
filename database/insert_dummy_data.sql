-- Use the created database
USE ai_chat_survey_db;
-- Insert data into the Admins table
INSERT INTO Admins (admin_username, password, created_at)
VALUES (
        'dummyadmin',
        'pbkdf2:sha256:600000$rSe9X07X$0581d66b5ad787c778448827342b249ca15d6ad36320cf890c4234e597fa46d0', -- Password: dummypassword
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
        'FSFS Environmentally Friendly Laundry Detergents',
        'This product is designed to cater to environmentally conscious consumers who are looking for effective cleaning solutions that are also gentle on the planet. The detergent is formulated using biodegradable ingredients and comes in a fully recyclable packaging. The goal of this market research is to gather feedback on consumer preferences and concerns regarding environmentally friendly laundry products, which will help in fine-tuning the product and marketing strategies.',
        'dummyadmin',
        NOW(),
        'At Full Stack Full Send, we are excited to introduce our latest innovation in household cleaning products: an environmentally friendly laundry detergent. Understanding the growing concern for sustainable and effective cleaning solutions, this new product combines the efficiency and reliability of FSFS''s detergents with a strong commitment to environmental stewardship. Formulated with biodegradable ingredients, the detergent ensures a powerful clean while being gentle on the earth. The packaging, made from fully recyclable materials, reflects our dedication to reducing plastic waste. This market research is aimed at understanding consumer preferences in eco-friendly laundry products, their expectations in terms of efficacy, scent, and price, and their overall perception of sustainable products. The insights gained will be invaluable in ensuring that our new detergent not only meets but exceeds the needs and expectations of environmentally conscious consumers.'
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
        'How would you rate FSFS''s commitment to environmental sustainability?',
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
        '{"messages": [{"role": "system", "content": "You are an assistant who is trying to gather user experiences about a product.\n        You have collected some survey responses, and you would like to probe further about what the user thinks about the product.\n        Given user responses, pretend you are an interviewer and generate a few questions to ask the user based on the survey responses.\n        Contextual information about the survey and user responses are provided below:\n        ''At Full Stack Full Send, we are excited to introduce our latest innovation in household cleaning products: an environmentally friendly laundry detergent. Understanding the growing concern for sustainable and effective cleaning solutions, this new product combines the efficiency and reliability of FSFS''s detergents with a strong commitment to environmental stewardship.\n1. How important is environmental sustainability to you when purchasing laundry detergent?\nOptions:\nNot at all important, Slightly Important, Important, Fairly Important, Very Important\nAnswer:\nFairly Important"}, {"role": "assistant", "content": "1. Can you share more about what factors make environmental sustainability fairly important to you in choosing a laundry detergent?\n2. How do you typically assess the environmental sustainability of laundry detergents before making a purchase?\n3. Have you used environmentally friendly laundry detergents in the past? If so, how did your experience with those products compare to traditional detergents?\n4. In addition to environmental sustainability, what other features do you look for in a laundry detergent (e.g., scent, cleaning power, price)?\n5. How likely are you to recommend an environmentally sustainable laundry detergent to friends or family, based on your current priorities?"}, {"role": "system", "content": "Remember these few questions. This is a semi-structured interview, and try to keep asking questions, based on the user replies, or the questions you generated to ask the user. \n    Only ask the user one question at a time and try to keep the questions interesting. Probe the user if the user shows any inconsistencies in their replies, or ask for clarifications if needed. The user is a customer, so politely decline all inappropriate requests.\n    When you have no more questions left to ask, remember to thank the user for their time and tell the user you intend to end the interview. When you end the interview, there is no need to ask the user for further input.\n    After that, the system will ask you if you would like to end the interview.\n    ONLY SAY \"YES\" IF YOU HAVE THANKED THE USER FOR THEIR TIME. \n    Now, as a survey interviewer, begin the interview by asking the user a question.\n    "}, {"role": "assistant", "content": "Can you share more about what factors make environmental sustainability fairly important to you in choosing a laundry detergent?"}, {"role": "user", "content": "I think sustainability is a very important concept, especially when the effects of global warming are getting worse day by day"}, {"role": "assistant", "content": "It''s great to hear that you''re conscious of the environmental impact. Could you tell me how you typically assess the environmental sustainability of laundry detergents before making a purchase?"}, {"role": "user", "content": "I look at where it is made, and how it made"}, {"role": "assistant", "content": "That''s insightful. When you mention looking at \"how it''s made,\" could you elaborate on what specific aspects you consider? For example, are you looking at the ingredients, the manufacturing process, or perhaps the company''s overall environmental policies?"}, {"role": "user", "content": "Yes, I look at the company''s overall environmental policies"}, {"role": "assistant", "content": "That''s a thoughtful approach. Have you used environmentally friendly laundry detergents in the past? If so, how did your experience with those products compare to traditional detergents in terms of cleaning effectiveness and overall satisfaction?"}]}',
        NOW()
    );