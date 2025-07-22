#!/usr/bin/env python3
"""
Simple test script to verify basic functionality
"""
import sys
import os

def test_imports():
    """Test basic imports"""
    try:
        print("Testing basic imports...")
        
        # Test pydantic
        from pydantic import BaseModel
        print("✅ Pydantic import successful")
        
        # Test FastAPI
        from fastapi import FastAPI
        print("✅ FastAPI import successful")
        
        # Test config
        from app.core.config import settings
        print(f"✅ Config import successful - PROJECT_NAME: {settings.PROJECT_NAME}")
        
        # Test database URL
        print(f"✅ Database URL: {settings.DATABASE_URL[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_app_creation():
    """Test FastAPI app creation"""
    try:
        print("\nTesting app creation...")
        from app.main import app
        print("✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running backend tests...\n")
    
    success = True
    success &= test_imports()
    success &= test_app_creation()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)