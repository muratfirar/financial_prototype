from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.company import RiskLevel, FinancialHealth, CompanyStatus

class CompanyBase(BaseModel):
    name: str
    tax_id: str
    sector: str
    revenue: Optional[float] = 0.0
    assets: Optional[float] = 0.0
    liabilities: Optional[float] = 0.0
    credit_limit: Optional[float] = 0.0

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    tax_id: Optional[str] = None
    sector: Optional[str] = None
    revenue: Optional[float] = None
    assets: Optional[float] = None
    liabilities: Optional[float] = None
    credit_limit: Optional[float] = None
    risk_score: Optional[int] = None
    risk_level: Optional[RiskLevel] = None
    pd_score: Optional[float] = None
    financial_health: Optional[FinancialHealth] = None
    status: Optional[CompanyStatus] = None

class CompanyInDBBase(CompanyBase):
    id: int
    risk_score: int
    risk_level: RiskLevel
    pd_score: float
    financial_health: FinancialHealth
    status: CompanyStatus
    last_analysis: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int

    class Config:
        from_attributes = True

class Company(CompanyInDBBase):
    pass

class CompanyWithMetrics(Company):
    equity: float
    debt_to_equity_ratio: Optional[float] = None
    latest_financial_metrics: Optional[dict] = None