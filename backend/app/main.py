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
    from app.api.v1 import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
except Exception as e:
    print(f"Warning: Could not load API routes: {e}")
    print("API will start with basic routes only")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.DEBUG
    )