#!/usr/bin/env python3
"""
Local development server starter
"""
import os
import sys

try:
    import uvicorn
except ImportError:
    print("❌ Error: uvicorn is not installed")
    print("📦 Installing required dependencies...")
    os.system("pip install uvicorn[standard]==0.24.0 fastapi==0.104.1 sqlalchemy==2.0.23 python-multipart==0.0.6 pydantic==2.5.0")
    import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Financial Risk Management Platform - Local Backend")
    print("📊 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("❤️ Health Check: http://localhost:8000/health")
    print()
    
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[script_dir]
    )