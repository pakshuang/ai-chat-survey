# Use an official Python runtime as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /src

# Create the requirements file from the Pipfile.lock
RUN pip install pipenv
COPY Pipfile.lock .
RUN pipenv requirements > requirements.txt
RUN pip uninstall -y pipenv

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY /src /src

# Expose the port on which the application will run
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Define the command to run the application
ENTRYPOINT ["streamlit", "run"]
CMD ["streamlit_app.py", "--server.address=0.0.0.0"]

# Build the Docker image
# docker build -t frontend .

# Run the Docker container
# docker run -p 8501:8501 frontend
