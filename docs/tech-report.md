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

## Installing the Application

1. Install [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/).

2. Initialise `.env` file (use `copy` for Windows CMD):

   ```shell
   cp sample.env .env
   ```

3. Fill in the `.env` file with the necessary environment variables. Some of the variables are already filled in with default values.

## Running the Application

To run the application, use the following command:

```shell
docker-compose up -d --build
```

If you want to horizontally scale (application level) the frontend or backend services, you can use the following command (do not scale the database service or nginx service):

```shell
docker-compose up -d --scale frontend=2 --scale backend=2
```

## Stopping the Application

To stop the application, use the following command:

```shell
docker-compose down
```

- Further details about setup/installation can be found in [Setup](setup.md), such as:
  - Backend Development Environment
  - Testing (Backend)
  - Frontend Development Environment

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
