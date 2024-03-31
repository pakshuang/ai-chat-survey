# Use an official Python runtime as the base image
FROM python:3.11.8

# Set the working directory in the container
WORKDIR /backend

# Copy the application code to the working directory
COPY src/ ./src
COPY tests/ ./tests
COPY Pipfile Pipfile.lock ./

# Install the dependencies
RUN pip install --no-cache-dir pipenv==2023.12.1 \
&& pipenv install --deploy

# Expose the port on which the application will run
EXPOSE ${BACKEND_CONTAINER_PORT}

# Define the command to run the application
CMD ["pipenv", "run", "python", "-m", "src.app"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${BACKEND_CONTAINER_PORT}/api/v1/health || exit 1