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

# Starting our application
CMD ["npm","run","dev"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${FRONTEND_CONTAINER_PORT}/admin/login || exit 1