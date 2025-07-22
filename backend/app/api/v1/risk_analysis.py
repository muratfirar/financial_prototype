from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import require_analyst_access
from app.models.user import User
from app.models.company import Company
from app.models.risk_analysis import RiskAnalysis
from app.models.financial_metric import FinancialMetric
from app.schemas.risk_analysis import (
    RiskAnalysis as RiskAnalysisSchema,
    RiskAnalysisCreate,
    RiskAnalysisUpdate,
    RiskAnalysisWithDetails
)
from app.services.risk_engine import RiskEngine
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[RiskAnalysisWithDetails])
def get_risk_analyses(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = None,
    analysis_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Get risk analyses with filtering
    """
    query = db.query(RiskAnalysis).join(Company).join(User)
    
    if company_id:
        query = query.filter(RiskAnalysis.company_id == company_id)
    
    if analysis_type:
        query = query.filter(RiskAnalysis.analysis_type == analysis_type)
    
    analyses = query.offset(skip).limit(limit).all()
    
    # Add company and analyst names
    result = []
    for analysis in analyses:
        company = db.query(Company).filter(Company.id == analysis.company_id).first()
        analyst = db.query(User).filter(User.id == analysis.analyst_id).first()
        
        analysis_dict = analysis.__dict__.copy()
        analysis_dict['company_name'] = company.name if company else "Unknown"
        analysis_dict['analyst_name'] = analyst.name if analyst else "Unknown"
        
        result.append(RiskAnalysisWithDetails(**analysis_dict))
    
    return result

@router.get("/{analysis_id}", response_model=RiskAnalysisWithDetails)
def get_risk_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Get specific risk analysis
    """
    analysis = db.query(RiskAnalysis).filter(RiskAnalysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk analysis not found"
        )
    
    company = db.query(Company).filter(Company.id == analysis.company_id).first()
    analyst = db.query(User).filter(User.id == analysis.analyst_id).first()
    
    analysis_dict = analysis.__dict__.copy()
    analysis_dict['company_name'] = company.name if company else "Unknown"
    analysis_dict['analyst_name'] = analyst.name if analyst else "Unknown"
    
    return RiskAnalysisWithDetails(**analysis_dict)

@router.post("/", response_model=RiskAnalysisSchema)
def create_risk_analysis(
    analysis_data: RiskAnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Create a new risk analysis
    """
    # Verify company exists
    company = db.query(Company).filter(Company.id == analysis_data.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Create analysis record
    db_analysis = RiskAnalysis(
        **analysis_data.dict(),
        analyst_id=current_user.id,
        status="in_progress"
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    # Schedule background analysis
    background_tasks.add_task(
        perform_risk_analysis,
        db_analysis.id,
        analysis_data.analysis_type
    )
    
    return db_analysis

@router.put("/{analysis_id}", response_model=RiskAnalysisSchema)
def update_risk_analysis(
    analysis_id: int,
    analysis_data: RiskAnalysisUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Update risk analysis
    """
    analysis = db.query(RiskAnalysis).filter(RiskAnalysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk analysis not found"
        )
    
    # Update analysis data
    update_data = analysis_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(analysis, field, value)
    
    db.commit()
    db.refresh(analysis)
    
    return analysis

@router.post("/{company_id}/quick-analysis")
def quick_risk_analysis(
    company_id: int,
    analysis_type: str = "credit",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Perform quick risk analysis and return immediate results
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
    
    # Perform analysis
    risk_engine = RiskEngine()
    
    if analysis_type == "credit":
        credit_score = risk_engine.calculate_credit_score(company, latest_metrics)
        recommended_limit = risk_engine.calculate_recommended_credit_limit(company, latest_metrics)
        risk_factors = risk_engine.generate_risk_factors(company, latest_metrics)
        
        return {
            "analysis_type": "credit",
            "credit_score": credit_score,
            "recommended_credit_limit": recommended_limit,
            "risk_factors": risk_factors,
            "timestamp": datetime.utcnow()
        }
    
    elif analysis_type == "pd":
        pd_score = risk_engine.calculate_pd_score(company, latest_metrics)
        risk_factors = risk_engine.generate_risk_factors(company, latest_metrics)
        
        return {
            "analysis_type": "pd",
            "pd_score": pd_score,
            "risk_level": "low" if pd_score < 5 else "medium" if pd_score < 10 else "high",
            "risk_factors": risk_factors,
            "timestamp": datetime.utcnow()
        }
    
    elif analysis_type == "stress_test":
        # Simplified stress test
        base_pd = risk_engine.calculate_pd_score(company, latest_metrics)
        
        scenarios = {
            "base_case": base_pd,
            "mild_stress": base_pd * 1.5,
            "moderate_stress": base_pd * 2.0,
            "severe_stress": base_pd * 3.0
        }
        
        return {
            "analysis_type": "stress_test",
            "scenarios": scenarios,
            "timestamp": datetime.utcnow()
        }
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid analysis type"
        )

def perform_risk_analysis(analysis_id: int, analysis_type: str):
    """
    Background task to perform detailed risk analysis
    """
    # This would be implemented as a background task
    # For now, we'll just update the status to completed
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        analysis = db.query(RiskAnalysis).filter(RiskAnalysis.id == analysis_id).first()
        if analysis:
            # Simulate analysis processing
            import time
            time.sleep(2)  # Simulate processing time
            
            analysis.status = "completed"
            analysis.confidence_level = 0.85
            db.commit()
    finally:
        db.close()