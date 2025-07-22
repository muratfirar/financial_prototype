from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class RiskAnalysis(Base):
    __tablename__ = "risk_analyses"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    analyst_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Analysis Type
    analysis_type = Column(String, nullable=False)  # credit, pd, stress_test
    
    # Risk Scores
    credit_score = Column(Integer, default=0)
    pd_score = Column(Float, default=0.0)
    lgd_score = Column(Float, default=0.0)  # Loss Given Default
    ead_score = Column(Float, default=0.0)  # Exposure at Default
    
    # Model Results
    model_version = Column(String, default="1.0")
    confidence_level = Column(Float, default=0.0)
    risk_factors = Column(JSON)  # Store risk factor weights
    
    # Recommendations
    recommended_credit_limit = Column(Float, default=0.0)
    risk_mitigation_actions = Column(Text)
    notes = Column(Text)
    
    # Status
    status = Column(String, default="completed")  # pending, in_progress, completed, failed
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="risk_analyses")
    analyst = relationship("User", back_populates="risk_analyses")