#!/bin/bash
set -e

echo "Starting Financial Risk Management Platform..."
echo "Port: $PORT"

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT