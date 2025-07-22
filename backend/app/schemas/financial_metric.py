from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FinancialMetricBase(BaseModel):
    company_id: int
    period: str
    revenue: Optional[float] = 0.0
    net_income: Optional[float] = 0.0
    gross_profit: Optional[float] = 0.0
    operating_income: Optional[float] = 0.0
    ebitda: Optional[float] = 0.0
    total_assets: Optional[float] = 0.0
    current_assets: Optional[float] = 0.0
    total_liabilities: Optional[float] = 0.0
    current_liabilities: Optional[float] = 0.0
    equity: Optional[float] = 0.0
    operating_cash_flow: Optional[float] = 0.0
    investing_cash_flow: Optional[float] = 0.0
    financing_cash_flow: Optional[float] = 0.0
    free_cash_flow: Optional[float] = 0.0
    debt_to_equity: Optional[float] = 0.0
    current_ratio: Optional[float] = 0.0
    quick_ratio: Optional[float] = 0.0
    roa: Optional[float] = 0.0
    roe: Optional[float] = 0.0

class FinancialMetricCreate(FinancialMetricBase):
    pass

class FinancialMetricUpdate(BaseModel):
    period: Optional[str] = None
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_income: Optional[float] = None
    ebitda: Optional[float] = None
    total_assets: Optional[float] = None
    current_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    current_liabilities: Optional[float] = None
    equity: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    investing_cash_flow: Optional[float] = None
    financing_cash_flow: Optional[float] = None
    free_cash_flow: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    roa: Optional[float] = None
    roe: Optional[float] = None

class FinancialMetricInDBBase(FinancialMetricBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FinancialMetric(FinancialMetricInDBBase):
    pass