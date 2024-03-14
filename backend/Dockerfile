# Use an official Python runtime as the base image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /src

# Create the requirements file from the Pipfile.lock
RUN pip install pipenv
COPY Pipfile.lock .
RUN pipenv requirements > requirements.txt
RUN pip uninstall -y pipenv

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY /src /src

# Expose the port on which the application will run
EXPOSE 5000

# Define the command to run the application
ENTRYPOINT ["python"]
CMD ["app.py"]

# Build the Docker image
# docker build -t backend .

# Run the Docker container
# docker run -p 5000:5000 backend