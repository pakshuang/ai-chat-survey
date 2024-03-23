# Use the official MySQL image as the base
FROM mysql:8.3.0

# Set the working directory in the container
WORKDIR /docker-entrypoint-initdb.d

# Copy the init.sql file into the container
COPY init.sql /docker-entrypoint-initdb.d/
COPY insert_dummy_data.sql /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306

# TODO: Set up volume mounts

