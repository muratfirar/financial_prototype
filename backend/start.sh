#!/bin/bash
set -e

echo "Starting Financial Risk Management Platform..."

# Run migrations with retry
echo "Running database migrations..."
python -c "
import time
import subprocess
import sys

max_retries = 10
for i in range(max_retries):
    try:
        result = subprocess.run(['alembic', 'upgrade', 'head'], check=True, capture_output=True, text=True)
        print('Migrations completed successfully')
        break
    except subprocess.CalledProcessError as e:
        print(f'Migration attempt {i+1}/{max_retries} failed: {e.stderr}')
        if i == max_retries - 1:
            print('All migration attempts failed')
            sys.exit(1)
        time.sleep(5)
"

# Create sample data with retry
echo "Creating sample data..."
python -c "
import time
import subprocess
import sys

max_retries = 5
for i in range(max_retries):
    try:
        result = subprocess.run(['python', 'create_sample_data.py'], check=True, capture_output=True, text=True)
        print('Sample data created successfully')
        break
    except subprocess.CalledProcessError as e:
        print(f'Sample data attempt {i+1}/{max_retries} failed: {e.stderr}')
        if i == max_retries - 1:
            print('Sample data creation failed, continuing anyway...')
        time.sleep(3)
"

# Start the application
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT