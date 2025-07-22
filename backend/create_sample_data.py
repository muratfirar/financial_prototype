"""
Script to create sample data for development and testing
"""
import sys
import os
import time
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models import *
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for development"""
    db = SessionLocal()
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create sample users
        users_data = [
            {
                "email": "admin@finansal.com",
                "name": "Sistem Yöneticisi",
                "role": UserRole.ADMIN,
                "password": "admin123"
            },
            {
                "email": "manager@finansal.com",
                "name": "Genel Müdür",
                "role": UserRole.MANAGER,
                "password": "manager123"
            },
            {
                "email": "analyst@finansal.com",
                "name": "Risk Analisti",
                "role": UserRole.RISK_ANALYST,
                "password": "analyst123"
            },
            {
                "email": "observer@finansal.com",
                "name": "Veri İzleyici",
                "role": UserRole.DATA_OBSERVER,
                "password": "observer123"
            },
            {
                "email": "dealer@finansal.com",
                "name": "Bayi Kullanıcı",
                "role": UserRole.DEALER,
                "password": "dealer123"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    name=user_data["name"],
                    role=user_data["role"],
                    hashed_password=get_password_hash(user_data["password"]),
                    is_active=True
                )
                db.add(user)
                created_users.append(user)
        
        db.commit()
        
        # Get the analyst user for company creation
        analyst_user = db.query(User).filter(User.role == UserRole.RISK_ANALYST).first()
        
        # Create sample companies
        companies_data = [
            {
                "name": "ABC Teknoloji A.Ş.",
                "tax_id": "1234567890",
                "sector": "Teknoloji",
                "revenue": 25000000,
                "assets": 15000000,
                "liabilities": 8000000,
                "credit_limit": 5000000,
                "risk_score": 750,
                "risk_level": RiskLevel.LOW,
                "pd_score": 2.3,
                "financial_health": FinancialHealth.GOOD,
                "status": CompanyStatus.ACTIVE
            },
            {
                "name": "DEF İnşaat Ltd.",
                "tax_id": "2345678901",
                "sector": "İnşaat",
                "revenue": 12000000,
                "assets": 20000000,
                "liabilities": 18000000,
                "credit_limit": 2000000,
                "risk_score": 520,
                "risk_level": RiskLevel.HIGH,
                "pd_score": 8.7,
                "financial_health": FinancialHealth.POOR,
                "status": CompanyStatus.MONITORING
            },
            {
                "name": "GHI Tekstil San.",
                "tax_id": "3456789012",
                "sector": "Tekstil",
                "revenue": 18000000,
                "assets": 12000000,
                "liabilities": 7500000,
                "credit_limit": 3500000,
                "risk_score": 680,
                "risk_level": RiskLevel.MEDIUM,
                "pd_score": 4.2,
                "financial_health": FinancialHealth.AVERAGE,
                "status": CompanyStatus.ACTIVE
            },
            {
                "name": "JKL Gıda A.Ş.",
                "tax_id": "4567890123",
                "sector": "Gıda",
                "revenue": 45000000,
                "assets": 30000000,
                "liabilities": 12000000,
                "credit_limit": 8000000,
                "risk_score": 820,
                "risk_level": RiskLevel.LOW,
                "pd_score": 1.8,
                "financial_health": FinancialHealth.EXCELLENT,
                "status": CompanyStatus.ACTIVE
            },
            {
                "name": "MNO Otomotiv Ltd.",
                "tax_id": "5678901234",
                "sector": "Otomotiv",
                "revenue": 8000000,
                "assets": 15000000,
                "liabilities": 16500000,
                "credit_limit": 1000000,
                "risk_score": 420,
                "risk_level": RiskLevel.CRITICAL,
                "pd_score": 15.2,
                "financial_health": FinancialHealth.CRITICAL,
                "status": CompanyStatus.MONITORING
            }
        ]
        
        for company_data in companies_data:
            # Check if company already exists
            existing_company = db.query(Company).filter(Company.tax_id == company_data["tax_id"]).first()
            if not existing_company:
                company = Company(
                    **company_data,
                    created_by=analyst_user.id,
                    last_analysis=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.add(company)
        
        db.commit()
        
        print("Sample data created successfully!")
        print("\nSample user credentials:")
        for user_data in users_data:
            print(f"Email: {user_data['email']}, Password: {user_data['password']}, Role: {user_data['role'].value}")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()