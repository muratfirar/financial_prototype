from pydantic_settings import BaseSettings
from typing import List
import os
import json

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://financial_user:financial_password@localhost:5432/financial_risk_db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PROJECT_NAME: str = "Financial Risk Management Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    _cors_origins: str = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:5173"]')
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        if isinstance(self._cors_origins, str):
            try:
                return json.loads(self._cors_origins)
            except json.JSONDecodeError:
                return [self._cors_origins]
        return self._cors_origins

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()