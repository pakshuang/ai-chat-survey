# Frontend Report

## Introduction

This section serves as an overview of the frontend architecture and design behind our web application. We explain the technical details of our implementation, as well as present the evolution of our interface and experience design based on dogfooding and user interviews, from our initial wireframes all the way to the final high-fidelity application.

## Architecture

### UI Libraries

We use React to leverage its modular approach, which allows developers to write smaller, self-contained components that can be put together and reused across different parts of an application to build complex user interfaces. React's virtual DOM also enhances performance by minimising unnecessary updates to the actual DOM, only re-rendering parts of the DOM that have changed. We also use Chakra UI's pre-made components to speed up the development process and ensure a consistent design across the application.

### Authentication

Users can authenticate into the admin portal using a username and password, whose validity is verified by the backend. Upon login, our backend sends a JWT, which is stored with the username in `localStorage`. Storing the JWT in memory was not chosen as it would require a new token with every page refresh, causing inconvenience. Furthermore, while storing the JWT in a same-site cookie would have been more secure, it is complicated to implement, and thus was not done due to time constraints. Storing the JWT in `localStorage` is still secure as it is not automatically sent with every HTTP request like cookies are, reducing the risk of CSRF (Cross-Site Request Forgery) attacks. `localStorage` access is also typically faster than cookie access.

### Authorization

Admin routes are protected, except the signup and login pages; unauthorized users who try to access admin routes will be redirected to the login page. Furthermore, admins are only authorized to access their own surveys and responses. Client routes, however, are accessible by everyone.

## Initial design

Our goal was to swiftly deliver a minimal viable product to our users, focusing on both functionality and aesthetics. To achieve this, we created low-fidelity wireframes and promptly developed them into a functional web application. We tested the app and gathered user feedback during interviews.

Note that our favicon, selected to illustrate the AI capabilities of our app, is by [Pexelpy](https://freeicons.io/profile/433683) on [freeicons.io](https://freeicons.io).

### Admin portal

Here are the initial wireframes for the various parts of admin portal. From left to right, top to bottom, we have the landing page, login page, signup page, admin homepage, new survey page, survey page, and survey responses page.

Admins are able to:

- Sign up and log into their account.
- View all surveys they have created in descending order of creation time.
- Create new surveys with titles, descriptions, and chat context, as well as MCQ, MRQs, and free response questions.
- View a survey and its responses, including the dynamic conversations with the chatbot.
- Delete a survey.
- Log out of their account.

<img src="wireframes/landing-page.png" width="32%"/> <img src="wireframes/login.png" width="32%"/> <img src="wireframes/signup.png" width="32%"/>

<img src="wireframes/admin-homepage.png" width="32%"/> <img src="wireframes/new-survey.png" width="32%"/>
<img src="wireframes/survey.png" width="32%"/>

<img src="wireframes/survey-responses.png" width="32%"/>

### Client interface

We aimed to maintain information collection efficiency while incorporating a conversational, chat-like format. This concept led us to develop two separate pages:

- Survey page: This is the page for static questions, i.e. questions that the surveyor wants all users to answer, allowing easy traditional quantitative analysis. Questions can be multiple choice, multiple response, and free response.
- Chat page: After the initial survey page, the user's answers are sent to a chatbot and users are redirected to the chat page where they engage in a conversation with the chatbot.

_images of the old form and chat page to be added_

## Initial user interviews

The following table shows the profiles of the users we interviewed.

| User | Profile                        |
| ---- | ------------------------------ |
| 1    | [age]-year-old [occupation]    |
| 2    | [age]-year-old [occupation]    |
| 3    | 22-year-old university student |
| 4    | Our business stakeholder       |

The following table shows their feedback, both positive and negative.

| User | Feedback                                                                                             | Change made? | Change in |
| ---- | ---------------------------------------------------------------------------------------------------- | ------------ | --------- |
| 1    | Unclear of importance of chat context                                                                | Yes          | Frontend  |
| 1    | Survey ending is abrupt                                                                              | Yes          | Backend   |
| 1    | Quite fun                                                                                            | NA           | NA        |
| 2    | Felt more compelled to continue the survey and give information because of the conversational nature | NA           | NA        |
| 3    | Add ability to include images, graphs                                                                | No           | Both      |
| 3    | Bot has the tendency to rephrase / repeat some questions                                             | Yes          | Backend   |
| 3    | Chat is quite responsive, feels natural                                                              | NA           | NA        |
| 4    | Consider security: prevent discriminatory words in LLM output                                        | Yes          | Backend   |
| 4    | Add ability to split the survey up into sections                                                     | No           | Both      |

Some user feedback required changes to the backend, not the frontend. We thus discuss these changes later in the backend section of the report. Furthermore, we did not implement a few changes due to time constraints (indicated by “No” in the “Change made” column), but could be added in the future.

## Final design

### Admin portal

The design of the admin portal was largely unaffected by our user interviews, which focused more on the client interface. However, based on User 1's feedback on their uncertainty about the importance of chat context, we added a tooltip to give more information on the importance of the chat context in generating good survey questions.

<img src="final-designs/chatbot-context-tooltip.png" width="50%"/>

Based on our own testing of our initial implementation, we also:

- Added a header to all admin pages to enable the user to check which account they're logged into and also log out easily

<img src="final-designs/header.png" width="50%"/>

Hovering over the avatar would reveal the current account's username.

- Added a section to each survey page to allow admins to easily test out the client interface
- Made survey description and chat context scroll vertically instead of horizontally for easier reading
  - In the screenshot below, note how the description and chat context are larger text boxes, rather than single lines of input as originally designed in the wireframe

<img src="final-designs/survey-interface-and-scroll.png" width="50%"/>

### Client interface

We implemented the following changes based on user feedback:

- Added a thank you message after the bot is done asking questions.
  The ending of the survey seems abrupt sometimes due to the bot's unpredictable nature. To ensure a smooth user experience, we implemented a flag that indicates whether the bot's message will be its last.
  _image of thank you message by bot to be added_
- Integrated survey page into chat page.
  Some users found the survey page's design and questions too similar to traditional surveys, reducing their desire to complete the survey. However, as business stakeholders still wanted the static questions to be asked, we could not remove the static questions entirely. Thus, we integrated them into the chat page to provide the experience of chatting with the LLM.
  _image of survey and image of chat from the chat page to be added_
- Displayed messages from bottom to top
  After the integration, we realised that the traditional way of showing messages from the top to bottom of the page might cause inconvenience for users at the beginning, who would have to go back and forth between reading the question at the top and filling out their answers in the chatbox at the bottom. Thus, we changed the direction of message display to position the latest question and chatbox close together.
  _image of first message that is from the bottom to be added_

## Follow-up user interviews

The following table shows feedback from our follow-up user interviews after refinements were made.

| User | Feedback                                                                             |
| ---- | ------------------------------------------------------------------------------------ |
| 4    | Chatbot's ability to ask good questions and clarify is great                         |
| 4    | Is it possible to add functionality to finetune a specific survey?                   |
| 4    | Can the chatbot be coerced to produce shorter messages?                              |
| 4    | Having the bot be able to take on specific personas would help keep the user engaged |

Some users further suggested features or enhancements that we could include; we address these in our Future Directions and Recommendations section.

## Conclusion

Our frontend has been thoughtfully designed with React and Chakra UI to craft a visually appealing, interactive interface that encourages user engagement. Authentication and authorization measures also secure admin routes and data, while future enhancements may explore more robust storage options. Overall, we have created a modern, engaging web application that can help boost survey completion rates and enhance product development with targeted qualitative feedback.
