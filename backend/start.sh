#!/bin/bash
set -e

echo "Starting Financial Risk Management Platform..."

# Test basic functionality first
echo "Running basic tests..."
python simple_test.py

if [ $? -eq 0 ]; then
    echo "✅ Basic tests passed"
else
    echo "❌ Basic tests failed, starting with minimal configuration"
fi

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT