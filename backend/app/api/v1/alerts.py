from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import require_read_access, require_analyst_access
from app.models.user import User
from app.models.risk_alert import RiskAlert
from app.models.company import Company
from app.schemas.risk_alert import RiskAlert as RiskAlertSchema, RiskAlertWithCompany, RiskAlertUpdate
from app.services.alert_service import AlertService

router = APIRouter()

@router.get("/", response_model=List[RiskAlertWithCompany])
def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    unread_only: bool = Query(False),
    severity: Optional[str] = Query(None),
    alert_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
):
    """
    Get risk alerts with filtering
    """
    query = db.query(RiskAlert).join(Company)
    
    # Apply filters
    if unread_only:
        query = query.filter(RiskAlert.is_read == False)
    
    if severity:
        query = query.filter(RiskAlert.severity == severity)
    
    if alert_type:
        query = query.filter(RiskAlert.alert_type == alert_type)
    
    # For dealers, only show alerts for their companies
    if current_user.role.value == "dealer":
        query = query.filter(Company.created_by == current_user.id)
    
    alerts = query.order_by(RiskAlert.created_at.desc()).offset(skip).limit(limit).all()
    
    # Add company names
    result = []
    for alert in alerts:
        company = db.query(Company).filter(Company.id == alert.company_id).first()
        alert_dict = alert.__dict__.copy()
        alert_dict['company_name'] = company.name if company else "Unknown"
        result.append(RiskAlertWithCompany(**alert_dict))
    
    return result

@router.get("/stats")
def get_alert_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
):
    """
    Get alert statistics
    """
    query = db.query(RiskAlert)
    
    # For dealers, only count alerts for their companies
    if current_user.role.value == "dealer":
        query = query.join(Company).filter(Company.created_by == current_user.id)
    
    total_alerts = query.count()
    unread_alerts = query.filter(RiskAlert.is_read == False).count()
    critical_alerts = query.filter(RiskAlert.severity == "critical").count()
    unresolved_alerts = query.filter(RiskAlert.is_resolved == False).count()
    
    return {
        "total_alerts": total_alerts,
        "unread_alerts": unread_alerts,
        "critical_alerts": critical_alerts,
        "unresolved_alerts": unresolved_alerts
    }

@router.put("/{alert_id}/read")
def mark_alert_as_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
):
    """
    Mark alert as read
    """
    alert = db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Check permissions for dealers
    if current_user.role.value == "dealer":
        company = db.query(Company).filter(Company.id == alert.company_id).first()
        if not company or company.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    alert_service = AlertService(db)
    success = alert_service.mark_alert_as_read(alert_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to mark alert as read"
        )
    
    return {"message": "Alert marked as read"}

@router.put("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Resolve an alert
    """
    alert = db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    alert_service = AlertService(db)
    success = alert_service.resolve_alert(alert_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to resolve alert"
        )
    
    return {"message": "Alert resolved successfully"}

@router.post("/generate/{company_id}")
def generate_alerts_for_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Manually generate alerts for a specific company
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    alert_service = AlertService(db)
    new_alerts = alert_service.check_and_generate_alerts(company)
    
    return {
        "message": f"Generated {len(new_alerts)} new alerts",
        "alert_count": len(new_alerts)
    }