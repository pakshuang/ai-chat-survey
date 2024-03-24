# Use an official Python runtime as the base image
FROM python:3.11.8-alpine

# Set the working directory in the container
WORKDIR /src

# Create the requirements file from the Pipfile.lock
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./

# Install the dependencies
RUN pipenv install --deploy

# Copy the rest of the application code to the working directory
COPY /src /src

# Expose the port on which the application will run
EXPOSE ${BACKEND_CONTAINER_PORT}

# Define the command to run the application
ENTRYPOINT ["pipenv", "run", "python"]
CMD ["app.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${BACKEND_CONTAINER_PORT}/api/v1/health || exit 1