#!/bin/bash

echo "🚀 Starting Financial Risk Management Platform - Local Development"
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check requirements
echo "🔍 Checking requirements..."
if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

echo "✅ Requirements check passed"
echo

# Start backend
echo "📊 Starting Backend (FastAPI)..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements-local.txt

# Start backend in background
echo "Starting FastAPI server..."
python app/main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend
echo
echo "🌐 Starting Frontend (React)..."
cd ..

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start frontend
echo "Starting Vite dev server..."
npm run dev &
FRONTEND_PID=$!

echo
echo "✅ Both services are starting!"
echo
echo "🔗 URLs:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo
echo "🔑 Test Users:"
echo "  admin@finansal.com / admin123"
echo "  analyst@finansal.com / analyst123"
echo
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
trap "echo; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait