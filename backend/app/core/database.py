from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from app.core.config import settings

def create_database_engine():
    """Create database engine with retry logic"""
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            database_url = settings.DATABASE_URL
            if not database_url or database_url == "":
                print(f"Attempt {attempt + 1}: DATABASE_URL is empty, waiting...")
                time.sleep(retry_delay)
                continue
                
            print(f"Attempt {attempt + 1}: Trying to connect to database...")
            
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                echo=settings.DEBUG,
                pool_recycle=300,
                pool_timeout=60,
                connect_args={
                    "connect_timeout": 60,
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
                # Don't raise exception, let the app start and retry later
                print("Creating engine anyway, connections will be retried at runtime...")
                return create_engine(
                    database_url if database_url else "sqlite:///./fallback.db",
                    pool_pre_ping=True,
                    echo=settings.DEBUG
                )
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