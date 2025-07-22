#!/bin/bash

echo "🚀 Starting Financial Risk Management Platform - Local Development"

echo
echo "📊 Starting Backend (FastAPI)..."
cd backend
python start_local.py &
BACKEND_PID=$!

echo
echo "⏳ Waiting for backend to start..."
sleep 5

echo
echo "🌐 Starting Frontend (React)..."
cd ..
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