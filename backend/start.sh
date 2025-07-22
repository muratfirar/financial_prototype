#!/bin/bash
set -e

echo "Starting Financial Risk Management Platform..."

# Wait for database
echo "Waiting for database..."
python wait-for-db.py

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Create sample data
echo "Creating sample data..."
python create_sample_data.py

# Start the application
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT