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
    recent_analyses = analyses_query.filter(
        func.date(RiskAnalysis.created_at) >= func.current_date() - func.interval('7 days')
    ).count()
    
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
        "recent_analyses": recent_analyses,
        "total_credit_exposure": total_credit_exposure,
        "average_risk_score": round(average_risk_score, 1),
        "average_pd_score": round(average_pd_score, 2),
        "high_risk_companies": high_risk_companies,
        "risk_distribution": risk_dist_dict
    }

@router.get("/recent-activities")
def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
) -> List[Dict[str, Any]]:
    """
    Get recent activities (analyses, alerts, company updates)
    """
    activities = []
    
    # Recent risk analyses
    analyses_query = db.query(RiskAnalysis).join(Company)
    if current_user.role.value == "dealer":
        analyses_query = analyses_query.filter(Company.created_by == current_user.id)
    
    recent_analyses = analyses_query.order_by(
        RiskAnalysis.created_at.desc()
    ).limit(limit // 2).all()
    
    for analysis in recent_analyses:
        company = db.query(Company).filter(Company.id == analysis.company_id).first()
        activities.append({
            "type": "analysis",
            "title": f"Risk analizi tamamlandı: {company.name if company else 'Unknown'}",
            "description": f"{analysis.analysis_type} analizi",
            "timestamp": analysis.created_at,
            "severity": "info"
        })
    
    # Recent alerts
    alerts_query = db.query(RiskAlert).join(Company)
    if current_user.role.value == "dealer":
        alerts_query = alerts_query.filter(Company.created_by == current_user.id)
    
    recent_alerts = alerts_query.order_by(
        RiskAlert.created_at.desc()
    ).limit(limit // 2).all()
    
    for alert in recent_alerts:
        company = db.query(Company).filter(Company.id == alert.company_id).first()
        activities.append({
            "type": "alert",
            "title": alert.title,
            "description": f"{company.name if company else 'Unknown'} - {alert.message}",
            "timestamp": alert.created_at,
            "severity": alert.severity.value
        })
    
    # Sort by timestamp and limit
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return activities[:limit]

@router.get("/risk-trends")
def get_risk_trends(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
) -> Dict[str, Any]:
    """
    Get risk trends over time
    """
    # This would typically involve time-series analysis
    # For now, return mock trend data
    
    import random
    from datetime import datetime, timedelta
    
    # Generate mock trend data
    dates = []
    risk_scores = []
    pd_scores = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i)
        dates.append(date.strftime("%Y-%m-%d"))
        
        # Mock trending data with some randomness
        base_risk = 650 + (i * 2) + random.randint(-20, 20)
        base_pd = 5.0 + (i * 0.1) + random.uniform(-0.5, 0.5)
        
        risk_scores.append(max(300, min(900, base_risk)))
        pd_scores.append(max(1.0, min(15.0, base_pd)))
    
    return {
        "dates": dates,
        "average_risk_scores": risk_scores,
        "average_pd_scores": pd_scores,
        "period_days": days
    }

@router.get("/sector-analysis")
def get_sector_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
) -> List[Dict[str, Any]]:
    """
    Get risk analysis by sector
    """
    companies_query = db.query(Company)
    
    if current_user.role.value == "dealer":
        companies_query = companies_query.filter(Company.created_by == current_user.id)
    
    sector_stats = db.query(
        Company.sector,
        func.count(Company.id).label('company_count'),
        func.avg(Company.risk_score).label('avg_risk_score'),
        func.avg(Company.pd_score).label('avg_pd_score'),
        func.sum(Company.credit_limit).label('total_exposure')
    ).group_by(Company.sector).all()
    
    result = []
    for stat in sector_stats:
        result.append({
            "sector": stat.sector,
            "company_count": stat.company_count,
            "average_risk_score": round(stat.avg_risk_score or 0, 1),
            "average_pd_score": round(stat.avg_pd_score or 0, 2),
            "total_credit_exposure": stat.total_exposure or 0,
            "risk_level": (
                "low" if (stat.avg_risk_score or 0) >= 750 else
                "medium" if (stat.avg_risk_score or 0) >= 600 else
                "high" if (stat.avg_risk_score or 0) >= 400 else
                "critical"
            )
        })
    
    return sorted(result, key=lambda x: x["total_credit_exposure"], reverse=True)