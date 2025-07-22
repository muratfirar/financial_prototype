#!/usr/bin/env python3
"""
Database reset script - removes old database and creates fresh one
"""
import os
import sys

def reset_database():
    """Reset the SQLite database"""
    db_file = "financial_risk.db"
    
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Removed old database: {db_file}")
    else:
        print(f"ℹ️ Database file not found: {db_file}")
    
    print("🔄 Database will be recreated when you start the server")
    print("🚀 Run: python start_local.py")

if __name__ == "__main__":
    reset_database()