from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import os

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic routes
@app.get("/")
def read_root():
    return {
        "message": "Financial Risk Management Platform API",
        "version": settings.VERSION,
        "docs_url": "/docs" if settings.DEBUG else None
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "port": os.getenv("PORT", "8000"),
        "environment": "production" if not settings.DEBUG else "development"
    }

# Include API router only if database is available
try:
    # Test database connection first
    from app.core.database import engine
    from sqlalchemy import text
    
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    
    print("✅ Database connection successful")
    
    from app.api.v1 import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    print("✅ API routes loaded successfully")
    
except Exception as e:
    print(f"❌ Could not load API routes: {e}")
    print("API will start with basic routes only")
    
    # Add a simple test route
    @app.get("/api/v1/test")
    def test_route():
        return {"message": "API is working", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.DEBUG
    )