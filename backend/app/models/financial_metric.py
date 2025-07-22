from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class FinancialMetric(Base):
    __tablename__ = "financial_metrics"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    period = Column(String, nullable=False)  # e.g., "2024-Q1", "2024-12"
    
    # Income Statement
    revenue = Column(Float, default=0.0)
    net_income = Column(Float, default=0.0)
    gross_profit = Column(Float, default=0.0)
    operating_income = Column(Float, default=0.0)
    ebitda = Column(Float, default=0.0)
    
    # Balance Sheet
    total_assets = Column(Float, default=0.0)
    current_assets = Column(Float, default=0.0)
    total_liabilities = Column(Float, default=0.0)
    current_liabilities = Column(Float, default=0.0)
    equity = Column(Float, default=0.0)
    
    # Cash Flow
    operating_cash_flow = Column(Float, default=0.0)
    investing_cash_flow = Column(Float, default=0.0)
    financing_cash_flow = Column(Float, default=0.0)
    free_cash_flow = Column(Float, default=0.0)
    
    # Financial Ratios
    debt_to_equity = Column(Float, default=0.0)
    current_ratio = Column(Float, default=0.0)
    quick_ratio = Column(Float, default=0.0)
    roa = Column(Float, default=0.0)  # Return on Assets
    roe = Column(Float, default=0.0)  # Return on Equity
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="financial_metrics")