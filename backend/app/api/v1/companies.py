from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.api.deps import get_current_active_user, require_analyst_access, require_read_access
from app.models.user import User
from app.models.company import Company
from app.schemas.company import Company as CompanySchema, CompanyCreate, CompanyUpdate

router = APIRouter()

@router.get("/", response_model=List[CompanySchema])
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
):
    """
    Get companies with filtering and pagination
    """
    query = db.query(Company)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Company.name.ilike(f"%{search}%"),
                Company.tax_id.ilike(f"%{search}%"),
                Company.sector.ilike(f"%{search}%")
            )
        )
    
    if risk_level:
        query = query.filter(Company.risk_level == risk_level)
    
    if sector:
        query = query.filter(Company.sector.ilike(f"%{sector}%"))
    
    # For dealers, only show their own companies
    if current_user.role.value == "dealer":
        query = query.filter(Company.created_by == current_user.id)
    
    companies = query.offset(skip).limit(limit).all()
    return companies

@router.get("/{company_id}", response_model=CompanySchema)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_read_access)
):
    """
    Get company by ID
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # For dealers, only allow access to their own companies
    if current_user.role.value == "dealer" and company.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return company

@router.post("/", response_model=CompanySchema)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Create a new company
    """
    # Check if company with same tax_id already exists
    existing_company = db.query(Company).filter(Company.tax_id == company_data.tax_id).first()
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this tax ID already exists"
        )
    
    # Create company
    db_company = Company(
        **company_data.dict(),
        created_by=current_user.id
    )
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.put("/{company_id}", response_model=CompanySchema)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Update company information
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Update company data
    update_data = company_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    
    return company

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
):
    """
    Delete a company (soft delete by setting status to inactive)
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Soft delete by setting status to inactive
    company.status = "inactive"
    db.commit()
    
    return {"message": "Company deleted successfully"}