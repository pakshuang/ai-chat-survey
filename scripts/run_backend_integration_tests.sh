#!/bin/bash
mv database/insert_dummy_data.sql .
docker compose down -v
rm backend/logs/integration_tests.log
docker compose -f compose.yaml -f compose.tests.yaml up integration-tests --build --force-recreate --renew-anon-volumes
docker compose -f compose.yaml -f compose.tests.yaml down -v
mv insert_dummy_data.sql database/