# Use an official PyTorch image with CUDA support as the base image
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Update Python version
RUN conda update -n base -c defaults conda && \
    conda install -y python=3.11.8 && \
    conda update --all --yes
  
# Set the working directory in the container
WORKDIR /backend-gpu

# Copy the application code to the working directory
COPY src/ ./src
COPY Pipfile Pipfile.lock ./

# Install the dependencies
RUN pip install --no-cache-dir pipenv==2023.12.1 \
&& pipenv install --deploy

# Define the command to run the application
CMD ["pipenv", "run", "python", "-m", "src.app"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${BACKEND_CONTAINER_PORT}/api/v1/health || exit 1