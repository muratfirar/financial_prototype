from fastapi import APIRouter
from app.api.v1 import auth, companies, dashboard, alerts, risk_analysis

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(risk_analysis.router, prefix="/risk-analysis", tags=["risk-analysis"])