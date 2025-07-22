#!/bin/bash
set -e

echo "Starting Financial Risk Management Platform..."

# Skip migrations during startup - will be done manually via Shell
echo "Skipping migrations (will be done manually via Render Shell)"

# Start the application directly
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT