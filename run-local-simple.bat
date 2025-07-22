@echo off
echo 🚀 Starting Financial Risk Management Platform - Local Development

echo.
echo 📊 Starting Backend (FastAPI)...
cd backend
start cmd /k "python start_local.py"

echo.
echo ⏳ Waiting for backend to start...
timeout /t 5

echo.
echo 🌐 Starting Frontend (React)...
cd ..
start cmd /k "npm run dev"

echo.
echo ✅ Both services are starting!
echo.
echo 🔗 URLs:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo 🔑 Test Users:
echo   admin@finansal.com / admin123
echo   analyst@finansal.com / analyst123
echo.
pause