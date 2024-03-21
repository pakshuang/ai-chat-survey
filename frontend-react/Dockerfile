# Fetching the latest node image on alpine linux
FROM node:alpine AS development

# Declaring env
ENV NODE_ENV development

# Setting up the work directory
WORKDIR /react-app

# Installing dependencies
COPY ./package*.json /react-app/

RUN npm install

# Copying all the files in our project
COPY . .

# Expose the port on which the application will run
EXPOSE 5173

# Starting our application
CMD ["npm","run","dev"]