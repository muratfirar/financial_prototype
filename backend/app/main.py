from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(
    title="Financial Risk Management Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic routes
@app.get("/")
def read_root():
    return {
        "message": "Financial Risk Management Platform API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "port": os.getenv("PORT", "8000"),
        "environment": "production"
    }

# Test route
@app.get("/api/v1/test")
def test_route():
    return {
        "message": "API is working",
        "status": "success"
    }

# Dashboard stats (mock data for now)
@app.get("/api/v1/dashboard/stats")
def get_dashboard_stats():
    return {
        "total_companies": 5,
        "active_companies": 4,
        "total_alerts": 3,
        "unread_alerts": 2,
        "critical_alerts": 1,
        "total_analyses": 12,
        "total_credit_exposure": 19500000,
        "average_risk_score": 654,
        "average_pd_score": 6.4,
        "high_risk_companies": 2,
        "risk_distribution": {
            "low": 2,
            "medium": 1,
            "high": 1,
            "critical": 1
        }
    }

# Companies endpoint (mock data)
@app.get("/api/v1/companies")
def get_companies():
    return [
        {
            "id": "1",
            "name": "ABC Teknoloji A.Ş.",
            "tax_id": "1234567890",
            "sector": "Teknoloji",
            "revenue": 25000000,
            "assets": 15000000,
            "liabilities": 8000000,
            "credit_limit": 5000000,
            "risk_score": 750,
            "risk_level": "low",
            "pd_score": 2.3,
            "financial_health": "good",
            "status": "active",
            "last_analysis": "2025-01-19",
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": 1
        },
        {
            "id": "2",
            "name": "DEF İnşaat Ltd.",
            "tax_id": "2345678901",
            "sector": "İnşaat",
            "revenue": 12000000,
            "assets": 20000000,
            "liabilities": 18000000,
            "credit_limit": 2000000,
            "risk_score": 520,
            "risk_level": "high",
            "pd_score": 8.7,
            "financial_health": "poor",
            "status": "monitoring",
            "last_analysis": "2025-01-18",
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": 1
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )