#!/usr/bin/env python3
"""
Wait for database to be ready before running migrations
"""
import os
import time
import psycopg2
from urllib.parse import urlparse

def wait_for_db():
    """Wait for database to be ready"""
    max_retries = 30
    retry_delay = 2
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found, skipping database wait")
        return
    
    # Parse database URL
    parsed = urlparse(database_url)
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:] if parsed.path else 'postgres'
            )
            conn.close()
            print(f"Database is ready! (attempt {attempt + 1})")
            return
            
        except psycopg2.OperationalError as e:
            print(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                print("Database connection timeout")
                raise
            time.sleep(retry_delay)

if __name__ == "__main__":
    wait_for_db()