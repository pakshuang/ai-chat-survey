# Frontend Report

## Introduction

This section serves as an overview of the frontend architecture and design behind our web application. We explain the technical details of our implementation, as well as present the evolution of our interface and experience design based on dogfooding and user interviews, from our initial wireframes all the way to the final high-fidelity application.

## Architecture

### Technologies Used and Justification

#### React

- Improved developer experience: React is easy to understand and with relatively small amount of code, developers can build robust and powerful app with desired animation and user experience. React allows developers to build highly interactive and responsive user interfaces, resulting in a smoother and more engaging experience for users.
- Code reusability: React is intuitive and promotes the concept of reusable components, which are self-contained modules that can be used across different parts of an application. This modular approach makes it easier to build complex user interfaces by breaking them down into smaller, reusable components.

#### Chakra UI

- Chakra UI supports React, and every component is customizable using the Style props. They map to almost all necessary CSS properties that are available.
- Simpler components: The best feature of Chakra UI is how components are designed to be small so that you can compose them together. You can build bigger elements easily by arranging them the same as HTML tags.
- Easy to theme and customize: One of the advantages of Chakra UI is that you can easily adjust it to your design needs.

#### Axios

- Axios is a popular JavaScript library used for making HTTP requests from a web browser. It provides an easy-to-use API that allows you to send asynchronous HTTP requests to a server and handle the responses.
- Easier syntax: The methods for different HTTP requests, such as GET and POST, are clearly defined in Axios. This results in more readable code and a shallower learning curve for new developers.
- Advanced and robust features: Axios comes packed with advanced features like request and response interceptors, automatic JSON data transformation, and configurable timeouts, which can save time for developers.

### Authentication and Authorization Considerations

- We use a simple set of username and password for admin authentication. Backend will then verify if the password matches with the username.
- Backend will send JWT token upon successful login, in which frontend will store the username and JWT in `localStorage`.
- Few alternatives to store the token include storing in memory or storing in cookie. Storing the token in a variable in memory is easy and hard to steal using an XSS (Cross-Site Scripting) attack, but a new token is needed every time the user refreshes the page, thus this option is not the most optimal for our app. Storing in a secure, same-site cookie is considered the most secure way to store JWT, but the implementation is complicated, hence we decided it's not worth the time and effort to implement this option. Therefore, we proceed with storing JWT in `localStorage` as it's easy to implement and tokens stored in `localStorage` are not automatically sent with every HTTP request like cookies are, reducing the risk of CSRF (Cross-Site Request Forgery) attacks. In addition, `localStorage` access is typically faster than cookie access. However, it's vulnerable to XSS attack. With these benefits and drawbacks in mind, we decided to go with `localStorage` implementation.
- We employed several authorization protections for admin routes. Admins can only access their surveys and responses list if they are logged in. Trying to manually change the url when they are not logged in will bring them to the login page. Furthermore, after login, admins can only access their own list of surveys and responses. They cannot access other admins' surveys. Trying to manually change the url to surveys they did not create will bring them to 404 Not Found page.
- Future development: Given more time, using secure, same-site cookie is preferable as it's more secure. Moreover, using UUID as survey's identifier is more secure, standardized, and professional as admins will not be able to guess other admins' survey UUID.

### Routing

- We use `react-router-dom` for our app routing. Admin routes are protected, except signup and login page. Accessing other admin routes without login will bring them to the login page.
- Client routes (chat page) are accessible by everyone. Accessing invalid routes will bring users to 404 Not Found page.

### Chat Page

- We design the Chat Page to provide users with a more engaging and interactive experience compared to traditional survey form. The simplistic look and chat-like design helps to replicate the feeling of conversing with a person.
- Messages displayed are retrieved from backend through an API call to ensure that the chat remains dynamic and responsive with real-time update and personalised interaction based on user input.
- Messages were displayed bottom-up as an UX consideration. We implemented messages to be displayed form top to bottom at first but after AB testing with our interviewees, we found that the bottom-up approach reduced time taken for the survey to be completed. This could be due to the difference in range of perception when one has answers at the bottom of the screen and the questions at the top.

## Initial design
s
Our goal was to swiftly deliver a minimal viable product to our users, focusing on both functionality and aesthetics. To achieve this, we created low-fidelity wireframes and promptly developed them into a functional web application. We tested the app and gathered user feedback during interviews.

Note that our favicon, selected to illustrate the AI capabilities of our app, is by [Pexelpy](https://freeicons.io/profile/433683) on [freeicons.io](https://freeicons.io).

### Admin portal

Here are the initial wireframes for the various parts of admin portal. From left to right, top to bottom, we have the landing page, login page, signup page, admin homepage, new survey page, survey page, and survey responses page.

Admins are able to:

- Signup and login to their account.
- View all surveys they have created, ordered in descending order based on their creation time.
- Create new surveys, provide survey title, description, and chat context to the GPT model, and specify questions with Multiple Choice, Multiple Responses, and Free Response format.
- View a specific survey and the responses of each surveys, including the conversations with the GPT model, after creating the survey.
- Delete a survey.
- Logout of their account.

<img src="wireframes/landing-page.png" width="32%"/> <img src="wireframes/login.png" width="32%"/> <img src="wireframes/signup.png" width="32%"/>

<img src="wireframes/admin-homepage.png" width="32%"/> <img src="wireframes/new-survey.png" width="32%"/>
<img src="wireframes/survey.png" width="32%"/>

<img src="wireframes/survey-responses.png" width="32%"/>

### Client interface

Our initial design approach for the client interface focuses on maintaining information collection efficiency while adapting the survey to have a conversational, chat-like format. This concept led us to develop two separate pages:

- Survey Form Page: This is the page for close-ended question, i.e. question that the surveyor would like to know regardless of the user's responses previously. The types of questions included on this page are multiple choice, multiple response, and free response.
- Chat Page: After the initial form page, the answers are sent to a chatbot and users are redirected to the chat page where they engage in a conversation with the chatbot.

_images of the old form and chat page to be added_

## Initial user interviews

The following table shows the profiles of the users we interviewed.

| User | Profile                     |
| ---- | --------------------------- |
| 1    | [age]-year-old [occupation] |
| 2    | [age]-year-old [occupation] |

The following table shows the feedback from each user as well as the refinements made for each piece of feedback.

| User | Feedback                              | Refinement                                                                    |
| ---- | ------------------------------------- | ----------------------------------------------------------------------------- |
| 1    | Unclear of importance of chat context | Emphasise importance of the chat context for the admin                        |
| 1    | Quite fun                             | NA                                                                            |
| 1    | Survey ending is abrupt               | Add final message to ask respondent if there’s anything else they want to add |

## Final design

### Admin portal

The design of the admin portal was largely unaffected by our user interviews, which focused more on the client interface. However, based on feedback on users' uncertainty about the importance of chat context, we added a tooltip to give more information on the importance of the chat context in generating good survey questions.

<img src="final-designs/chatbot-context-tooltip.png"/>

Based on our dogfooding of our initial implementation, we also:

- Added a header to all admin pages to enable the user to check which account they're logged into and also log out easily

<img src="final-designs/header.png"/>

Hovering over the avatar would reveal the current account's username.

- Added a section to each survey page to allow admins to easily test out the client interface
- Made survey description and chat context scroll vertically instead of horizontally for easier reading
  - In the screenshot below, note how the description and chat context are larger text boxes, rather than single lines of input as originally designed in the wireframe

<img src="final-designs/survey-interface-and-scroll.png"/>

### Client interface

We received numerous feedbacks and implemented changes accordingly. Here are the changes:

- Add thank you message after the bot is done asking questions.
  The ending of the survey seems abrupt sometimes due to the nature of the bot that we cannot predict. To ensure a smooth experience for the user, we implemented a flag which indicates whether the message from the bot is the last message.
  _image of thank you message by bot to be added_
- Integrate form page into chat page.
  The design of the survey form page receives a lot of criticism due to its resemblance of the old traditional survey form. While doing the first part of the survey, some of the users stopped doing it since it is not too appealing. Since the workflow requires close-ended questions to be asked first, we decided to bring everything into the chat page.
  _image of survey and image of chat from the chat page to be added_
- Display messages from bottom to top
  After the integration, we realise that it is not a good idea to keep the messages from top to bottom as the question may be on top, yet the choices is at the bottom of the page. We want the users to be comfortable in viewing questions and the choices together, so we change the direction of displaying the messages.
  _image of first message that is from the bottom to be added_

## Follow-up user interviews

- Rubrics: Repeat consults with user.

The following table shows the feedback from each user after refinements were made.

| User | Feedback |
| ---- | -------- |
| 1    |          |

## Conclusion

The frontend architecture and design has undergone a thoughtful evolution, driven by user feedback and iterative design cycles. Our focus on creating a user-friendly experience has resulted in a modern and engaging web application.

Key components like React, Chakra UI, and Axios have been instrumental in delivering a visually appealing and interactive interface. The integration of form elements within the Chat Page has enhanced user engagement and streamlined the survey completion process.

Authentication and authorization measures have been implemented to ensure secure access to admin routes and protect user data. While current storage methods like localStorage serve our needs, future enhancements may explore more secure options.

Overall, our frontend architecture strikes a balance between technical sophistication and user-centric design, culminating in a successful implementation that meets the needs of our users and project goals.