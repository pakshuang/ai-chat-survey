# Use the official MySQL image as the base
FROM mysql:8.3.0

# Set the working directory in the container
WORKDIR /docker-entrypoint-initdb.d

# Copy the init.sql file into the container
COPY init.sql /docker-entrypoint-initdb.d/

# TODO: Set up volume mounts

