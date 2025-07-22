#!/usr/bin/env python3
"""
Local development server starter
"""
import uvicorn
import os
import sys

if __name__ == "__main__":
    print("🚀 Starting Financial Risk Management Platform - Local Backend")
    print("📊 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("❤️ Health Check: http://localhost:8000/health")
    print()
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[backend_dir]
    )