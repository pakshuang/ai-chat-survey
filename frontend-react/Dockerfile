# Fetching the latest node image on alpine linux
FROM node:alpine AS build-stage

# Setting up the work directory
WORKDIR /react-app

# Installing dependencies
COPY ./package*.json /react-app/

RUN npm install

# Copying all the files in our project
COPY . .

# Building the static files
RUN npm run build

# Fetching the latest nginx image on alpine linux
FROM nginx:alpine
COPY --from=build-stage /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/admin/login || exit 1