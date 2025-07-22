from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.api.deps import get_current_active_user, require_analyst_access, require_read_access
from app.models.user import User
from app.models.company import Company
from app.models.financial_metric import FinancialMetric
from app.schemas.company import Company as CompanySchema, CompanyCreate, CompanyUpdate, CompanyWithMetrics
from app.services.risk_engine import RiskEngine
from app.services.alert_service import AlertService

router = APIRouter()

@router.get("/", response_model=List[CompanySchema])
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
):
    """
    Get companies with filtering and pagination
    """
    query = db.query(Company)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Company.name.ilike(f"%{search}%"),
                Company.tax_id.ilike(f"%{search}%"),
                Company.sector.ilike(f"%{search}%")
            )
        )
    
    if risk_level:
        query = query.filter(Company.risk_level == risk_level)
    
    if sector:
        query = query.filter(Company.sector.ilike(f"%{sector}%"))
    
    # For dealers, only show their own companies
    if current_user.role.value == "dealer":
        query = query.filter(Company.created_by == current_user.id)
    
    companies = query.offset(skip).limit(limit).all()
    return companies

@router.get("/{company_id}", response_model=CompanyWithMetrics)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
):
    """
    Get company by ID with detailed metrics
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # For dealers, only allow access to their own companies
    if current_user.role.value == "dealer" and company.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Calculate additional metrics
    equity = company.assets - company.liabilities
    debt_to_equity_ratio = company.liabilities / max(equity, 1) if equity > 0 else None
    
    # Get latest financial metrics
    latest_metrics = db.query(FinancialMetric).filter(
        FinancialMetric.company_id == company_id
    ).order_by(FinancialMetric.created_at.desc()).first()
    
    latest_financial_metrics = None
    if latest_metrics:
        latest_financial_metrics = {
            "period": latest_metrics.period,
            "revenue": latest_metrics.revenue,
            "net_income": latest_metrics.net_income,
            "current_ratio": latest_metrics.current_ratio,
            "debt_to_equity": latest_metrics.debt_to_equity,
            "roa": latest_metrics.roa,
            "roe": latest_metrics.roe
        }
    
    return CompanyWithMetrics(
        **company.__dict__,
        equity=equity,
        debt_to_equity_ratio=debt_to_equity_ratio,
        latest_financial_metrics=latest_financial_metrics
    )

@router.post("/", response_model=CompanySchema)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Create a new company
    """
    # Check if company with same tax_id already exists
    existing_company = db.query(Company).filter(Company.tax_id == company_data.tax_id).first()
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this tax ID already exists"
        )
    
    # Create company
    db_company = Company(
        **company_data.dict(),
        created_by=current_user.id
    )
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    # Calculate initial risk scores
    risk_engine = RiskEngine()
    db_company.risk_score = risk_engine.calculate_credit_score(db_company)
    db_company.pd_score = risk_engine.calculate_pd_score(db_company)
    
    # Determine risk level based on score
    if db_company.risk_score >= 750:
        db_company.risk_level = "low"
        db_company.financial_health = "good"
    elif db_company.risk_score >= 600:
        db_company.risk_level = "medium"
        db_company.financial_health = "average"
    elif db_company.risk_score >= 400:
        db_company.risk_level = "high"
        db_company.financial_health = "poor"
    else:
        db_company.risk_level = "critical"
        db_company.financial_health = "critical"
    
    db.commit()
    db.refresh(db_company)
    
    # Generate alerts if necessary
    alert_service = AlertService(db)
    alert_service.check_and_generate_alerts(db_company)
    
    return db_company

@router.put("/{company_id}", response_model=CompanySchema)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Update company information
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Update company data
    update_data = company_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    # Recalculate risk scores if financial data changed
    financial_fields = ['revenue', 'assets', 'liabilities']
    if any(field in update_data for field in financial_fields):
        risk_engine = RiskEngine()
        company.risk_score = risk_engine.calculate_credit_score(company)
        company.pd_score = risk_engine.calculate_pd_score(company)
        
        # Update recommended credit limit
        recommended_limit = risk_engine.calculate_recommended_credit_limit(company)
        if company.credit_limit == 0:  # Only update if not manually set
            company.credit_limit = recommended_limit
    
    db.commit()
    db.refresh(company)
    
    # Check for new alerts
    alert_service = AlertService(db)
    alert_service.check_and_generate_alerts(company)
    
    return company

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Delete a company (soft delete by setting status to inactive)
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Soft delete by setting status to inactive
    company.status = "inactive"
    db.commit()
    
    return {"message": "Company deleted successfully"}

@router.post("/{company_id}/recalculate-risk")
def recalculate_company_risk(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Manually trigger risk recalculation for a company
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Get latest financial metrics
    latest_metrics = db.query(FinancialMetric).filter(
        FinancialMetric.company_id == company_id
    ).order_by(FinancialMetric.created_at.desc()).first()
    
    # Recalculate risk scores
    risk_engine = RiskEngine()
    company.risk_score = risk_engine.calculate_credit_score(company, latest_metrics)
    company.pd_score = risk_engine.calculate_pd_score(company, latest_metrics)
    
    # Update risk level based on new score
    if company.risk_score >= 750:
        company.risk_level = "low"
    elif company.risk_score >= 600:
        company.risk_level = "medium"
    elif company.risk_score >= 400:
        company.risk_level = "high"
    else:
        company.risk_level = "critical"
    
    # Update financial health
    if company.pd_score < 2:
        company.financial_health = "excellent"
    elif company.pd_score < 5:
        company.financial_health = "good"
    elif company.pd_score < 10:
        company.financial_health = "average"
    elif company.pd_score < 20:
        company.financial_health = "poor"
    else:
        company.financial_health = "critical"
    
    company.last_analysis = db.func.now()
    db.commit()
    db.refresh(company)
    
    # Generate new alerts if necessary
    alert_service = AlertService(db)
    alert_service.check_and_generate_alerts(company)
    
    return {
        "message": "Risk calculation completed",
        "risk_score": company.risk_score,
        "pd_score": company.pd_score,
        "risk_level": company.risk_level.value,
        "financial_health": company.financial_health.value
    }