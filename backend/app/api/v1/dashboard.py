from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.api.deps import require_read_access
from app.models.user import User
from app.models.company import Company
from app.models.risk_alert import RiskAlert
from app.models.risk_analysis import RiskAnalysis

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
) -> Dict[str, Any]:
    """
    Get dashboard statistics
    """
    # Base queries
    companies_query = db.query(Company)
    alerts_query = db.query(RiskAlert)
    analyses_query = db.query(RiskAnalysis)
    
    # Filter for dealers - only their companies
    if current_user.role.value == "dealer":
        companies_query = companies_query.filter(Company.created_by == current_user.id)
        alerts_query = alerts_query.join(Company).filter(Company.created_by == current_user.id)
        analyses_query = analyses_query.join(Company).filter(Company.created_by == current_user.id)
    
    # Get basic counts
    total_companies = companies_query.count()
    active_companies = companies_query.filter(Company.status == "active").count()
    
    # Risk distribution
    risk_distribution = db.query(
        Company.risk_level,
        func.count(Company.id).label('count')
    ).group_by(Company.risk_level).all()
    
    risk_dist_dict = {level: 0 for level in ['low', 'medium', 'high', 'critical']}
    for level, count in risk_distribution:
        risk_dist_dict[level.value] = count
    
    # Alert statistics
    total_alerts = alerts_query.count()
    unread_alerts = alerts_query.filter(RiskAlert.is_read == False).count()
    critical_alerts = alerts_query.filter(RiskAlert.severity == "critical").count()
    
    # Analysis statistics
    total_analyses = analyses_query.count()
    
    # Financial metrics
    total_credit_exposure = db.query(func.sum(Company.credit_limit)).scalar() or 0
    average_risk_score = db.query(func.avg(Company.risk_score)).scalar() or 0
    average_pd_score = db.query(func.avg(Company.pd_score)).scalar() or 0
    
    # High risk companies
    high_risk_companies = companies_query.filter(
        Company.risk_level.in_(["high", "critical"])
    ).count()
    
    return {
        "total_companies": total_companies,
        "active_companies": active_companies,
        "total_alerts": total_alerts,
        "unread_alerts": unread_alerts,
        "critical_alerts": critical_alerts,
        "total_analyses": total_analyses,
        "total_credit_exposure": total_credit_exposure,
        "average_risk_score": round(average_risk_score, 1),
        "average_pd_score": round(average_pd_score, 2),
        "high_risk_companies": high_risk_companies,
        "risk_distribution": risk_dist_dict
    }