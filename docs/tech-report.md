# Tech Report

## Table of Contents
1. [Intro](#intro)
2. [Setup/Installation](#setupinstallation)
3. [Overall Architecture](#overall-architecture)
4. [Frontend](#frontend)
5. [Backend](#backend)
6. [Future Directions and Recommendations](#future-directions-and-recommendations)
7. [Conclusion](#conclusion)

## Intro
- Insert intro

## Setup/Installation
1. Clone the repository:

   ```shell
   git clone https://github.com/pakshuang/ai-chat-survey.git
   ```

2. Change into the project directory:

   ```shell
   cd ai-chat-survey
   ```

3. Initialise `.env` file:
   Windows CMD:

   ```shell
   copy sample.env .env
   ```

   Unix:

   ```shell
   cp sample.env .env
   ```

4. Fill in the `.env` file with the necessary environment variables. Some of the variables are already filled in with default values.

## Running the Application

To run the application, use the following command:

```shell
docker-compose up -d --build
```

If you have already built the images, you can use the following command to start the application:

```shell
docker-compose up -d
```

If you want to horizontally scale (application level) the frontend or backend services, you can use the following command (do not scale the database service or nginx service):

```shell
docker-compose up -d --scale frontend=2 --scale backend=2
```

During development, you may want to run the application on a clean slate. To do this, you can use the following command:

```shell
docker-compose up -d --build --force-recreate --renew-anon-volumes
```

## Stopping the Application

To stop the application, use the following command:

```shell
docker-compose down
```

During development, you may want to stop the application and remove all images and volumes. To do this, you can use the following command:

```shell
docker-compose down --rmi all --volumes
```
- For more detailed setup/installation instructions such as:
  - Backend Development Environment
  - Testing (Backend)
  - Frontend Development Environment

  please visit [setup.md](setup.md).

## Overall Architecture
- Insert description of the overall architecture goes here.

## Frontend
- [Frontend](frontend.md): Insert Description and details about the frontend components and technologies used.

## Backend
- [Backend](backend.md): Insert Description and details about the backend components and technologies used.

## Future Directions and Recommendations
- [Localisation](localisation.md)

## Conclusion
- Insert conclusion goes here.