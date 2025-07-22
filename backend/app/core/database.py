from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from app.core.config import settings

def create_database_engine():
    """Create database engine with retry logic"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            database_url = settings.DATABASE_URL
            if not database_url or database_url == "":
                print(f"Attempt {attempt + 1}: DATABASE_URL is empty, waiting...")
                time.sleep(retry_delay)
                continue
           
           print(f"Attempt {attempt + 1}: Trying to connect to database...")
           print(f"Database URL host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'unknown'}")
                
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                echo=settings.DEBUG,
                pool_recycle=300,
               pool_timeout=30,
               connect_args={
                   "connect_timeout": 30,
                   "application_name": "financial_risk_platform"
               }
            )
            
            # Test connection
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            
            print(f"Database connection successful on attempt {attempt + 1}")
            return engine
            
        except Exception as e:
            print(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print("All database connection attempts failed")
               print(f"Final DATABASE_URL: {settings.DATABASE_URL}")
                raise
            time.sleep(retry_delay)
    
    raise Exception("Could not establish database connection")

# Create engine with retry logic
engine = create_database_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()