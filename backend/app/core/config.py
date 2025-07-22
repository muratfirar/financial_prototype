from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    @property
    def DATABASE_URL(self) -> str:
        # Try different environment variable names that Render might use
        db_url = (
            os.getenv("DATABASE_URL") or 
            os.getenv("POSTGRES_URL") or 
            os.getenv("DB_URL") or
            os.getenv("INTERNAL_DATABASE_URL") or
            "postgresql://financial_user:financial_password@localhost:5432/financial_risk_db"
        )
        
        # Handle postgres:// vs postgresql:// URL schemes
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        return db_url
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 

settings = Settings()