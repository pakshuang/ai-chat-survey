# Tech Report

## Table of Contents

1. [Intro](#intro)
2. [Setup](#setup)
3. [Overall Architecture](#overall-architecture)
4. [Frontend](#frontend)
5. [Backend](#backend)
6. [DevOps](#devops)
7. [Future Directions and Recommendations](#future-directions-and-recommendations)
8. [Conclusion](#conclusion)

## Intro
In today's rapidly evolving business landscape, understanding customer needs and preferences is the cornerstone of success. Traditional survey methods, while informative, often fall short in capturing the intricacies of consumer behavior and sentiment.

In this report, we unveil a proof-of-concept project poised to revolutionize the way businesses conduct customer research. Leveraging the power of Large Language Models (LLMs), particularly GPT-4, we're introducing a dynamic and personalized survey experience that transcends the limitations of conventional approaches.

Our vision is simple yet transformative: to create surveys that adapt in real-time based on each respondent's unique input. By integrating GPT-4 into our survey platform, we're not only collecting data but engaging customers in meaningful conversations. This innovative approach enables us to pursue unique lines of inquiry, uncovering insights that traditional surveys often miss.

## Setup

### Installing the Application

1. Install [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/).

2. Initialise `.env` file (use `copy` for Windows CMD):

   ```shell
   cp sample.env .env
   ```

3. Fill in the `.env` file with the necessary environment variables. Some of the variables are already filled in with default values.

### Running the Application

```shell
docker-compose up -d --build
```

If you want to horizontally scale (application level) the frontend or backend services, you can use the following command (do not scale the database service or nginx service):

```shell
docker-compose up -d --scale frontend=2 --scale backend=2
```

### Stopping the Application

```shell
docker-compose down
```

Further details about setup/installation can be found in [Setup](setup.md), such as:

- Backend Development Environment
- Testing (Backend)
- Frontend Development Environment
- Deployment

## Overall Architecture

![Architecture](diagrams/images/overall-architecture.png)

### Services

- **Reverse Proxy (Nginx)**: Handles incoming requests and routes them to the backend or frontend. This unifies the frontend and backend under a single domain and allows for easy scaling of the frontend and backend services as well as avoids CORS issues.
- **SSL Certificate Client (Certbot)**: Automatically fetches and renews SSL certificates from Let's Encrypt. This ensures that the application is served over HTTPS, providing a secure connection for users.
- **Frontend (React)**: User interface for the application. It can be scaled horizontally to handle more users.
- **Backend (Flask)**: Handles the business logic and interacts with the database. It can be scaled horizontally to handle more users.
- **Database (MySQL)**: Stores the data for the application.

### Technology Stack

- **Reverse Proxy (Nginx)**: Nginx was chosen due to its simplicity and performance. It is used to route requests to the frontend or backend based on the URL path. Load balancing relies on the Docker network's internal DNS resolution. For more advanced load balancing, solutions like Traefik can be used due to its dynamic configuration capabilities and support for Docker.
- **SSL Certificate Client (Certbot)**: Certbot was chosen for its ease of use and integration with Let's Encrypt.
- The rationale for the choice of technologies for the other services can be found in the respective sections below.


## DevOps

- **Docker**: The application is split into multiple services (frontend, backend, database, nginx) and each service is containerised using Docker.
- **Docker Compose**: The application is orchestrated using Docker Compose. This allows for easy management and deployment of the application and its services. The `docker-compose.yml` file defines the services, environment variables, bind mounts, etc. for the application. Overlapping or alternate compose files are used for additional purposes such as integration testing and model evaluation.
- **GitHub Repository**: The codebase is hosted on a mono-repo on GitHub. This allows for easy access to all parts of the application and ensures that all parts are versioned together. The repository is private and access is restricted to team members.
- **GitHub Pull Requests**: Features are developed on separate branches and merged regularly. Pull requests are used to merge changes into the main branch. Pull requests require approval from code owners of the files changed and must pass the CI pipeline before they can be merged.
- **GitHub Actions**: Continuous Integration (CI) is set up using GitHub Actions. The CI pipeline runs linters to ensure proper formatting as well as integration tests to ensure the application is working as expected. These checks are automated and are required to pass before a pull request can be merged.
- **GitHub Issues**: Issues are used to track tasks, bugs, and enhancements. They are labelled and assigned to team members to keep track of progress.
- **Bash Scripts**: Bash scripts are used to automate common tasks such as local integration testing.
- **Telegram**: A private Telegram group is used for communication between team members. The group uses the "Topics" feature to categorise messages into different topics such as "General", "Frontend", "API", "BRD", "Pull Requests", etc.

## Future Directions and Recommendations

### Additional Features

Expanding on the initial capabilities of our platform, we envision a variety of enhancements to enrich the user experience and increase the platform's utility:

- **Adding Sections**: Based on extensive user interviews and feedback from our business stakeholders, we've identified a significant improvement for our survey platform: the integration of distinct sections. This enhancement will effectively create multiple "mini-surveys" within a single session. Respondents will alternate between answering predefined questions from the organization and engaging in interactive conversations with GPT-4. This enables more effective detection and documentation of inconsistencies in respondents' feedback within the survey session itself, improving the quality and reliability of the data collected.
- **Editable Surveys:** Introduce the ability to modify surveys after they have been created, allowing users to adapt and improve their surveys based on initial feedback and insights.
- **Multimedia Support:** Enable the inclusion of images, videos, and audio clips within surveys to provide a richer respondent experience and capture more nuanced feedback.
- **Real-time Analytics Dashboard:** Develop a dashboard that provides real-time analytics and insights into survey responses. This tool could help survey creators quickly understand trends and adjust their strategies accordingly.
- **Multi-language Support:** Offer surveys in multiple languages to reach a broader audience. This feature would be particularly valuable for global companies looking to gather insights across different demographics.
- **Integration with CRM Systems:** Provide integration options with customer relationship management (CRM) systems to seamlessly sync survey data with existing customer profiles. This would enhance the ability to track customer satisfaction and engagement over time.
- **Automated Report Generation:** Add functionality for automatic generation of comprehensive reports based on survey results, including graphical representations of data and key metrics summaries.

These features aim to make the survey platform not only more interactive and engaging for respondents but also more insightful and effective for researchers and businesses. By continuously evolving the platform, we can better meet the diverse needs of our users and stay ahead in the competitive field of customer research.

### Analyzing ChatLogs
- Since all chat logs and survey responses are stored in our database, it becomes a valuable resource for further downstream analysis. 
- Techniques such as sentiment analysis, topic modeling, and clustering can be employed to extract deeper insights into customer interactions and preferences. 
- By leveraging platforms like [Inari](https://www.ycombinator.com/launches/Kpg-inari-ai-powered-product-discovery-and-feedback-analytics), which is designed for AI-powered feedback analytics, organizations can enhance their understanding of customer feedback, ultimately driving product development and enhancement.

### Local LLMs
In the modern data-centric environment, companies prioritize safeguarding sensitive information while enhancing operational efficiency. To achieve these goals, leveraging Local Language Models (LLMs) becomes crucial. While LLMs are accessible via APIs, relying solely on external services can pose risks, especially if these APIs cease to provide LLM support, causing disruptions. Furthermore, maintaining data privacy is paramount for companies, making it essential to avoid sharing sensitive information with external API providers when interacting with a model. Deploying LLMs internally helps mitigate these risks and ensures data remains secure within the organization's infrastructure.

We have written a skeleton for this future extension. In particular, we have provided a working [finetuning script](https://github.com/pakshuang/ai-chat-survey/blob/main/scripts/finetuning/GPTQLoRA-script.py) for GPTQ-quantised LLMs using a GPU, as well as a dockerised container that has access to a GPU and can load a localised LLM. We have also written a document for users to use the finetuning scripts and running the docker container. Please refer to [localisation.md](https://github.com/pakshuang/ai-chat-survey/blob/main/docs/localisation.md).

The LLM scene is constantly evolving. On April 18, 2024, Meta released llama-3, a very capable open-source LLM. Llama-3 comes in two sizes, 70b and 8b. The 8b model is the most capable open-source model for its weight class, to date. To speak of its impressiveness, as of 24 April 2024, it is currently (ranked 14 in the Overall category on the Chatbot Arena)[https://chat.lmsys.org/?leaderboard], a leaderboard where human evaluators rate the effectiveness of LLMs against one another. The 8-billion parameter model performs much above its weight class and ranks alongside Mistral-Medium (rank 14), Gemini 1.0 Pro (Dev API) (rank 21), both of which are much larger closed-source models. GPT-3.5-Turbo-0613 is ranked 25.

The 70-billion parameter version is also very impressive. As of 24 April 2024, it has a rank of 6 in the Overall category, above two snapshots of GPT-4 (GPT-4-0314: rank 9, GPT-4-0613: rank 12) and Claude 3 Sonnet (rank 7).

Such improvements are certain to keep coming, and it would be a good idea to keep on the lookout for upcoming models. A good place to source for good models would be:
(Chatbot Arena)[https://chat.lmsys.org/?leaderboard] - A site where human evaluators rate the effectiveness of LLMs in general or specific tasks like coding

(Open LLM leaderboard)[https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard] - A site where LLMs are rated on a variety of benchmarks like TruthfulQA (A dataset that evaluates on mitigating falsehoods).

## Conclusion

In conclusion, our project has demonstrated the potential of integrating GPT-4 into customer research surveys, offering a glimpse into a future where technology enhances the survey experience. While our endeavor may be modest in scope, its implications are significant.

Through our proof of concept, we've showcased the feasibility of leveraging GPT-4 to personalize survey interactions and uncover unique insights from respondents. By adopting this approach, businesses can gain a deeper understanding of customer preferences and feedback, ultimately guiding strategic decision-making processes.

While our project may be a small step, it symbolizes a larger shift towards more dynamic and engaging survey methodologies. As technology continues to evolve, opportunities abound for further exploration and refinement in this field.
