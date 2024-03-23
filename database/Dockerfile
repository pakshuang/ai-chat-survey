# Use the official MySQL image as the base
FROM mysql:8.3.0

# Set the working directory in the container
WORKDIR /docker-entrypoint-initdb.d

# Copy the init.sql file into the container
COPY init.sql /docker-entrypoint-initdb.d/
COPY insert_dummy_data.sql /docker-entrypoint-initdb.d/

# TODO: Set up volume mounts

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD mysqladmin ping -h localhost -u root --password=${MYSQL_ROOT_PASSWORD} || exit 1