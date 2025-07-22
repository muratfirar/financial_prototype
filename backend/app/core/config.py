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
            "postgresql://financial_user:financial_password@localhost:5432/financial_risk_db"
        )
        
        # Handle postgres:// vs postgresql:// URL schemes
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        return db_url
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "your-super-secret-key-here-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PROJECT_NAME: str = "Financial Risk Management Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    @property
    def CORS_ORIGINS(self) -> List[str]:
        if self.DEBUG:
            return ["*"]
        return [
            "http://localhost:3000",
            "http://localhost:5173", 
            "https://financial-risk-frontend.onrender.com"
        ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()