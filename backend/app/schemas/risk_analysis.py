from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class RiskAnalysisBase(BaseModel):
    company_id: int
    analysis_type: str
    credit_score: Optional[int] = 0
    pd_score: Optional[float] = 0.0
    lgd_score: Optional[float] = 0.0
    ead_score: Optional[float] = 0.0
    model_version: Optional[str] = "1.0"
    confidence_level: Optional[float] = 0.0
    risk_factors: Optional[Dict[str, Any]] = None
    recommended_credit_limit: Optional[float] = 0.0
    risk_mitigation_actions: Optional[str] = None
    notes: Optional[str] = None

class RiskAnalysisCreate(RiskAnalysisBase):
    pass

class RiskAnalysisUpdate(BaseModel):
    analysis_type: Optional[str] = None
    credit_score: Optional[int] = None
    pd_score: Optional[float] = None
    lgd_score: Optional[float] = None
    ead_score: Optional[float] = None
    confidence_level: Optional[float] = None
    risk_factors: Optional[Dict[str, Any]] = None
    recommended_credit_limit: Optional[float] = None
    risk_mitigation_actions: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class RiskAnalysisInDBBase(RiskAnalysisBase):
    id: int
    analyst_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RiskAnalysis(RiskAnalysisInDBBase):
    pass

class RiskAnalysisWithDetails(RiskAnalysis):
    company_name: str
    analyst_name: str