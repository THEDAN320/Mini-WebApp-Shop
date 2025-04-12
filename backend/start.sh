#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
/dev_backend/.venv/bin/alembic -c models/alembic.ini upgrade head

# Start the application
echo "Starting the application..."
exec /dev_backend/.venv/bin/fastapi run main.py --port 8000 --host 0.0.0.0 --reload
