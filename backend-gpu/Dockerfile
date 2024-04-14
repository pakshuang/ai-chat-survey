# Use an official PyTorch image with CUDA support as the base image
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set the working directory in the container
WORKDIR /backend-gpu

# Copy the application code to the working directory
COPY src/ ./src
COPY models/ ./models
COPY Pipfile Pipfile.lock ./

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
# Install necessary packages to allow compilation of source code
    && apt-get install -y --no-install-recommends \
    tzdata \
    build-essential \
    checkinstall \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    software-properties-common \
    && apt-get update \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y --no-install-recommends \
    python3.11.8

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11.8
# Install the dependencies
RUN pip install --no-cache-dir pipenv==2023.12.1 \
&& pipenv install --deploy

# Define the command to run the application
CMD ["pipenv", "run", "python", "-m", "src.app"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${BACKEND_CONTAINER_PORT}/api/v1/health || exit 1