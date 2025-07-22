from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    @property
    def DATABASE_URL(self) -> str:
        # Render.com internal database URL - use internal hostname
        db_url = os.getenv("DATABASE_URL")
        
        if not db_url:
            # Fallback to default for local development
            return "postgresql://financial_user:financial_password@localhost:5432/financial_risk_db"
        
        # Convert external hostname to internal for Render.com
        if "dpg-" in db_url and "-a/" in db_url:
            # Replace external hostname with internal
            # External: dpg-xxx-a
            # Internal: dpg-xxx-a.oregon-postgres.render.com
            db_url = db_url.replace("@dpg-", "@dpg-").replace("-a/", "-a.oregon-postgres.render.com/")
        
        # Handle postgres:// vs postgresql:// URL schemes
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        return db_url
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 

settings = Settings()