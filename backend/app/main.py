from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import enum
import os

# Database setup (SQLite for local development)
SQLALCHEMY_DATABASE_URL = "sqlite:///./financial_risk.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
from app.api.v1 import api_router

# Database Models
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    RISK_ANALYST = "risk_analyst"
    DATA_OBSERVER = "data_observer"
    DEALER = "dealer"

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

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tax_id = Column(String, unique=True, index=True)
    sector = Column(String)
    revenue = Column(Float, default=0.0)
    assets = Column(Float, default=0.0)
    liabilities = Column(Float, default=0.0)
    credit_limit = Column(Float, default=0.0)
    risk_score = Column(Integer, default=0)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    pd_score = Column(Float, default=0.0)
    financial_health = Column(Enum(FinancialHealth), default=FinancialHealth.AVERAGE)
    status = Column(Enum(CompanyStatus), default=CompanyStatus.ACTIVE)
    last_analysis = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, default=1)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatar: Optional[str] = None

class CompanyResponse(BaseModel):
    id: str
    name: str
    tax_id: str
    sector: str
    revenue: float
    assets: float
    liabilities: float
    credit_limit: float
    risk_score: int
    risk_level: str
    pd_score: float
    financial_health: str
    status: str
    last_analysis: str
    created_at: str
    created_by: int

class CompanyCreate(BaseModel):
    name: str
    tax_id: str
    sector: str
    revenue: Optional[float] = 0.0
    assets: Optional[float] = 0.0
    liabilities: Optional[float] = 0.0
    credit_limit: Optional[float] = 0.0

# FastAPI app
app = FastAPI(
    title="Financial Risk Management Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock authentication (simple for local development)
def authenticate_user(email: str, password: str):
    # Simple mock authentication
    mock_users = {
        "admin@finansal.com": {"password": "admin123", "role": "admin", "name": "Sistem Yöneticisi"},
        "analyst@finansal.com": {"password": "analyst123", "role": "risk_analyst", "name": "Risk Analisti"},
        "manager@finansal.com": {"password": "manager123", "role": "manager", "name": "Yönetici"},
    }
    
    if email in mock_users and mock_users[email]["password"] == password:
        return mock_users[email]
    return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Simple token validation (in production, use proper JWT)
    if token.startswith("mock_token_"):
        email = token.split("_")[2]
        mock_users = {
            "admin@finansal.com": {"id": "1", "role": "admin", "name": "Sistem Yöneticisi"},
            "analyst@finansal.com": {"id": "2", "role": "risk_analyst", "name": "Risk Analisti"},
            "manager@finansal.com": {"id": "3", "role": "manager", "name": "Yönetici"},
        }
        if email in mock_users:
            user_data = mock_users[email]
            return UserResponse(
                id=user_data["id"],
                name=user_data["name"],
                email=email,
                role=user_data["role"]
            )
    raise HTTPException(status_code=401, detail="Invalid token")

# Initialize database with sample data
def init_sample_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Company).count() > 0:
            return
        
        # Add sample companies
        companies = [
            Company(
                name="ABC Teknoloji A.Ş.",
                tax_id="1234567890",
                sector="Teknoloji",
                revenue=25000000,
                assets=15000000,
                liabilities=8000000,
                credit_limit=5000000,
                risk_score=750,
                risk_level=RiskLevel.LOW,
                pd_score=2.3,
                financial_health=FinancialHealth.GOOD,
                status=CompanyStatus.ACTIVE,
                last_analysis="2025-01-19"
            ),
            Company(
                name="DEF İnşaat Ltd.",
                tax_id="2345678901",
                sector="İnşaat",
                revenue=12000000,
                assets=20000000,
                liabilities=18000000,
                credit_limit=2000000,
                risk_score=520,
                risk_level=RiskLevel.HIGH,
                pd_score=8.7,
                financial_health=FinancialHealth.POOR,
                status=CompanyStatus.MONITORING,
                last_analysis="2025-01-18"
            ),
            Company(
                name="GHI Tekstil San.",
                tax_id="3456789012",
                sector="Tekstil",
                revenue=18000000,
                assets=12000000,
                liabilities=7500000,
                credit_limit=3500000,
                risk_score=680,
                risk_level=RiskLevel.MEDIUM,
                pd_score=4.2,
                financial_health=FinancialHealth.AVERAGE,
                status=CompanyStatus.ACTIVE,
                last_analysis="2025-01-20"
            ),
            Company(
                name="JKL Gıda A.Ş.",
                tax_id="4567890123",
                sector="Gıda",
                revenue=45000000,
                assets=30000000,
                liabilities=12000000,
                credit_limit=8000000,
                risk_score=820,
                risk_level=RiskLevel.LOW,
                pd_score=1.8,
                financial_health=FinancialHealth.EXCELLENT,
                status=CompanyStatus.ACTIVE,
                last_analysis="2025-01-19"
            ),
            Company(
                name="MNO Otomotiv Ltd.",
                tax_id="5678901234",
                sector="Otomotiv",
                revenue=8000000,
                assets=15000000,
                liabilities=16500000,
                credit_limit=1000000,
                risk_score=420,
                risk_level=RiskLevel.CRITICAL,
                pd_score=15.2,
                financial_health=FinancialHealth.CRITICAL,
                status=CompanyStatus.MONITORING,
                last_analysis="2025-01-20"
            )
        ]
        
        for company in companies:
            db.add(company)
        
        db.commit()
        print("✅ Sample data initialized")
        
    except Exception as e:
        print(f"❌ Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()

# Routes
@app.get("/")
def read_root():
    return {
        "message": "Financial Risk Management Platform API - Local Development",
        "version": "1.0.0",
        "status": "running",
        "environment": "local"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": "local",
        "database": "sqlite"
    }

@app.post("/api/v1/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create simple token
    access_token = f"mock_token_{form_data.username}_{form_data.password}"
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@app.get("/api/v1/companies", response_model=List[CompanyResponse])
def get_companies(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    risk_level: Optional[str] = None,
    sector: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Company)
    
    if search:
        query = query.filter(
            (Company.name.contains(search)) |
            (Company.tax_id.contains(search)) |
            (Company.sector.contains(search))
        )
    
    if risk_level:
        query = query.filter(Company.risk_level == risk_level)
    
    if sector:
        query = query.filter(Company.sector.contains(sector))
    
    companies = query.offset(skip).limit(limit).all()
    
    return [
        CompanyResponse(
            id=str(company.id),
            name=company.name,
            tax_id=company.tax_id,
            sector=company.sector,
            revenue=company.revenue,
            assets=company.assets,
            liabilities=company.liabilities,
            credit_limit=company.credit_limit,
            risk_score=company.risk_score,
            risk_level=company.risk_level.value,
            pd_score=company.pd_score,
            financial_health=company.financial_health.value,
            status=company.status.value,
            last_analysis=company.last_analysis or "",
            created_at=company.created_at.isoformat() if company.created_at else "",
            created_by=company.created_by
        )
        for company in companies
    ]

@app.get("/api/v1/companies/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        tax_id=company.tax_id,
        sector=company.sector,
        revenue=company.revenue,
        assets=company.assets,
        liabilities=company.liabilities,
        credit_limit=company.credit_limit,
        risk_score=company.risk_score,
        risk_level=company.risk_level.value,
        pd_score=company.pd_score,
        financial_health=company.financial_health.value,
        status=company.status.value,
        last_analysis=company.last_analysis or "",
        created_at=company.created_at.isoformat() if company.created_at else "",
        created_by=company.created_by
    )

@app.post("/api/v1/companies", response_model=CompanyResponse)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    # Check if company with same tax_id exists
    existing = db.query(Company).filter(Company.tax_id == company_data.tax_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company with this tax ID already exists")
    
    # Create new company
    db_company = Company(
        name=company_data.name,
        tax_id=company_data.tax_id,
        sector=company_data.sector,
        revenue=company_data.revenue,
        assets=company_data.assets,
        liabilities=company_data.liabilities,
        credit_limit=company_data.credit_limit,
        created_by=int(current_user.id),
        last_analysis=datetime.now().strftime("%Y-%m-%d")
    )
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return CompanyResponse(
        id=str(db_company.id),
        name=db_company.name,
        tax_id=db_company.tax_id,
        sector=db_company.sector,
        revenue=db_company.revenue,
        assets=db_company.assets,
        liabilities=db_company.liabilities,
        credit_limit=db_company.credit_limit,
        risk_score=db_company.risk_score,
        risk_level=db_company.risk_level.value,
        pd_score=db_company.pd_score,
        financial_health=db_company.financial_health.value,
        status=db_company.status.value,
        last_analysis=db_company.last_analysis or "",
        created_at=db_company.created_at.isoformat() if db_company.created_at else "",
        created_by=db_company.created_by
    )

@app.get("/api/v1/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_companies = db.query(Company).count()
    active_companies = db.query(Company).filter(Company.status == CompanyStatus.ACTIVE).count()
    
    # Risk distribution
    risk_counts = {}
    for level in RiskLevel:
        count = db.query(Company).filter(Company.risk_level == level).count()
        risk_counts[level.value] = count
    
    # Calculate averages
    companies = db.query(Company).all()
    avg_risk_score = sum(c.risk_score for c in companies) / len(companies) if companies else 0
    avg_pd_score = sum(c.pd_score for c in companies) / len(companies) if companies else 0
    total_credit_exposure = sum(c.credit_limit for c in companies)
    high_risk_companies = db.query(Company).filter(
        Company.risk_level.in_([RiskLevel.HIGH, RiskLevel.CRITICAL])
    ).count()
    
    return {
        "total_companies": total_companies,
        "active_companies": active_companies,
        "total_alerts": 3,  # Mock data
        "unread_alerts": 2,  # Mock data
        "critical_alerts": 1,  # Mock data
        "total_analyses": 12,  # Mock data
        "total_credit_exposure": total_credit_exposure,
        "average_risk_score": round(avg_risk_score, 1),
        "average_pd_score": round(avg_pd_score, 2),
        "high_risk_companies": high_risk_companies,
        "risk_distribution": risk_counts
    }

# Initialize sample data on startup
@app.on_event("startup")
def startup_event():
    init_sample_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)