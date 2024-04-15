
FROM nvidia/cuda:11.8.0-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /backend-gpu

# Update package lists and install dependencies
RUN apt-get update && \
    apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev wget

# Download and install Python 3.11.8


RUN wget https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tar.xz && \
    tar -xf Python-3.11.8.tar.xz && \
    cd Python-3.11.8 && \
    ./configure --enable-optimizations --with-ensurepip=install && \
    make -j $(nproc) && \
    make altinstall

# Clean up unnecessary files
RUN rm -rf /tmp/Python-3.11.8*

# Verify Python installation
RUN apt-get install -y python3-pip

# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
# Install the dependencies
RUN pip3 install --no-cache-dir pipenv==2023.12.1


# Copy the application code to the working directory
COPY src/ ./src
COPY models/ ./models
COPY Pipfile Pipfile.lock ./


RUN pipenv install --system --python python3.11.8
RUN pipenv install --verbose



# Define the command to run the application
CMD ["pipenv", "run", "python", "-m", "src.app"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${BACKEND_CONTAINER_PORT}/api/v1/health || exit 1