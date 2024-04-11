#!/bin/bash

# Store the first command line argument as the number of backend instances
BACKEND_INSTANCES=${1:-1}  # Default to 1 if no argument is provided

# Move the SQL file for dummy data
mv database/insert_dummy_data.sql .

# Bring down any existing containers and volumes
docker compose down -v

# Remove the existing integration test log file
rm -f backend/logs/integration_tests.log

# Run Docker Compose and scale the backend service
docker compose -f compose.yaml -f compose.tests.yaml up integration-tests --build --force-recreate --renew-anon-volumes --scale backend=$BACKEND_INSTANCES

# Bring down the containers and volumes after the test
docker compose -f compose.yaml -f compose.tests.yaml down -v

# Move the SQL file back to its original location
mv insert_dummy_data.sql database/
