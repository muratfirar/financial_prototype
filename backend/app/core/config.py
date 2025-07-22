from pydantic_settings import BaseSettings
from typing import List
import os
import re

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Financial Risk Management Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    @property
    def DATABASE_URL(self) -> str:
        # Get database URL from environment
        db_url = os.getenv("DATABASE_URL")
        
        if not db_url:
            # Fallback for local development
            return "postgresql://financial_user:financial_password@localhost:5432/financial_risk_db"
        
        # Convert external Render hostname to internal
        if "dpg-" in db_url and not ".oregon-postgres.render.com" in db_url:
            # Replace external hostname with internal
            # External: dpg-xxx-a
            # Internal: dpg-xxx-a.oregon-postgres.render.com
            db_url = re.sub(r'@(dpg-[^/]+)/', r'@\1.oregon-postgres.render.com/', db_url)
        
        # Handle postgres:// vs postgresql:// URL schemes
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        return db_url
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Configuration
    @property
    def CORS_ORIGINS(self) -> List[str]:
        # Default CORS origins
        if self.DEBUG:
            return [
                "http://localhost:3000",
                "http://localhost:5173",
                "http://127.0.0.1:3000", 
                "http://127.0.0.1:5173",
                "https://financial-risk-frontend.onrender.com"
            ]
        else:
            return [
                "https://financial-risk-frontend.onrender.com",
                "https://*.onrender.com",
                "*"
            ]

settings = Settings()