from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class FinancialHealth(str, enum.Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    CRITICAL = "critical"

class CompanyStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MONITORING = "monitoring"

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    tax_id = Column(String, unique=True, nullable=False, index=True)
    sector = Column(String, nullable=False)
    
    # Risk Information
    risk_score = Column(Integer, default=0)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    pd_score = Column(Float, default=0.0)  # Probability of Default
    financial_health = Column(Enum(FinancialHealth), default=FinancialHealth.AVERAGE)
    
    # Financial Data
    revenue = Column(Float, default=0.0)
    assets = Column(Float, default=0.0)
    liabilities = Column(Float, default=0.0)
    credit_limit = Column(Float, default=0.0)
    
    # Status and Dates
    status = Column(Enum(CompanyStatus), default=CompanyStatus.ACTIVE)
    last_analysis = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by_user = relationship("User", back_populates="created_companies")
    financial_metrics = relationship("FinancialMetric", back_populates="company")
    risk_analyses = relationship("RiskAnalysis", back_populates="company")
    risk_alerts = relationship("RiskAlert", back_populates="company")