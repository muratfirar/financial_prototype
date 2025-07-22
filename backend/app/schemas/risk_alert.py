from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.risk_alert import AlertType, AlertSeverity

class RiskAlertBase(BaseModel):
    company_id: int
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    threshold_value: Optional[str] = None
    current_value: Optional[str] = None

class RiskAlertCreate(RiskAlertBase):
    pass

class RiskAlertUpdate(BaseModel):
    alert_type: Optional[AlertType] = None
    severity: Optional[AlertSeverity] = None
    title: Optional[str] = None
    message: Optional[str] = None
    threshold_value: Optional[str] = None
    current_value: Optional[str] = None
    is_read: Optional[bool] = None
    is_resolved: Optional[bool] = None

class RiskAlertInDBBase(RiskAlertBase):
    id: int
    is_read: bool
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RiskAlert(RiskAlertInDBBase):
    pass

class RiskAlertWithCompany(RiskAlert):
    company_name: str