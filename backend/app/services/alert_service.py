from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.risk_alert import RiskAlert, AlertType, AlertSeverity
from app.models.company import Company
from app.models.financial_metric import FinancialMetric
from app.schemas.risk_alert import RiskAlertCreate
from datetime import datetime, timedelta

class AlertService:
    """
    Service for generating and managing risk alerts
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_and_generate_alerts(self, company: Company) -> List[RiskAlert]:
        """
        Check company data and generate alerts if thresholds are exceeded
        """
        alerts = []
        
        # Check PD Score Alert
        if company.pd_score > 10.0:
            alert = self._create_pd_alert(company)
            if alert:
                alerts.append(alert)
        
        # Check Credit Limit Usage
        alert = self._check_credit_limit_usage(company)
        if alert:
            alerts.append(alert)
        
        # Check Financial Deterioration
        alert = self._check_financial_deterioration(company)
        if alert:
            alerts.append(alert)
        
        # Check Payment Delays (if monitoring status)
        if company.status.value == "monitoring":
            alert = self._create_payment_delay_alert(company)
            if alert:
                alerts.append(alert)
        
        return alerts
    
    def _create_pd_alert(self, company: Company) -> Optional[RiskAlert]:
        """Create PD increase alert"""
        # Check if similar alert already exists in last 7 days
        recent_alert = self.db.query(RiskAlert).filter(
            RiskAlert.company_id == company.id,
            RiskAlert.alert_type == AlertType.PD_INCREASE,
            RiskAlert.created_at > datetime.utcnow() - timedelta(days=7)
        ).first()
        
        if recent_alert:
            return None
        
        severity = AlertSeverity.CRITICAL if company.pd_score > 15 else AlertSeverity.HIGH
        
        alert_data = RiskAlertCreate(
            company_id=company.id,
            alert_type=AlertType.PD_INCREASE,
            severity=severity,
            title=f"PD Skoru Yüksek Risk: {company.name}",
            message=f"PD skoru %{company.pd_score:.1f} seviyesine yükseldi. Acil risk değerlendirmesi gerekli.",
            threshold_value="10.0%",
            current_value=f"{company.pd_score:.1f}%"
        )
        
        alert = RiskAlert(**alert_data.dict())
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        
        return alert
    
    def _check_credit_limit_usage(self, company: Company) -> Optional[RiskAlert]:
        """Check credit limit usage and create alert if necessary"""
        # This would typically check actual credit usage vs limit
        # For demo purposes, we'll simulate based on company data
        
        if company.liabilities > company.credit_limit * 0.8:
            usage_percentage = (company.liabilities / company.credit_limit) * 100
            
            severity = AlertSeverity.CRITICAL if usage_percentage > 95 else AlertSeverity.HIGH
            
            alert_data = RiskAlertCreate(
                company_id=company.id,
                alert_type=AlertType.CREDIT_LIMIT,
                severity=severity,
                title=f"Kredi Limit Uyarısı: {company.name}",
                message=f"Kredi kullanım oranı %{usage_percentage:.1f} seviyesinde. Limit aşım riski var.",
                threshold_value="80%",
                current_value=f"{usage_percentage:.1f}%"
            )
            
            alert = RiskAlert(**alert_data.dict())
            self.db.add(alert)
            self.db.commit()
            self.db.refresh(alert)
            
            return alert
        
        return None
    
    def _check_financial_deterioration(self, company: Company) -> Optional[RiskAlert]:
        """Check for financial deterioration"""
        if company.financial_health.value in ["poor", "critical"]:
            severity = AlertSeverity.CRITICAL if company.financial_health.value == "critical" else AlertSeverity.HIGH
            
            alert_data = RiskAlertCreate(
                company_id=company.id,
                alert_type=AlertType.FINANCIAL_DETERIORATION,
                severity=severity,
                title=f"Finansal Durum Kötüleşmesi: {company.name}",
                message=f"Finansal sağlık durumu '{company.financial_health.value}' seviyesine düştü.",
                current_value=company.financial_health.value
            )
            
            alert = RiskAlert(**alert_data.dict())
            self.db.add(alert)
            self.db.commit()
            self.db.refresh(alert)
            
            return alert
        
        return None
    
    def _create_payment_delay_alert(self, company: Company) -> Optional[RiskAlert]:
        """Create payment delay alert for companies under monitoring"""
        alert_data = RiskAlertCreate(
            company_id=company.id,
            alert_type=AlertType.PAYMENT_DELAY,
            severity=AlertSeverity.MEDIUM,
            title=f"Ödeme Takip Uyarısı: {company.name}",
            message="Firma izleme listesinde. Ödeme performansı yakından takip ediliyor.",
            current_value="monitoring"
        )
        
        alert = RiskAlert(**alert_data.dict())
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        
        return alert
    
    def mark_alert_as_read(self, alert_id: int, user_id: int) -> bool:
        """Mark alert as read"""
        alert = self.db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
        if alert:
            alert.is_read = True
            self.db.commit()
            return True
        return False
    
    def resolve_alert(self, alert_id: int, user_id: int) -> bool:
        """Resolve an alert"""
        alert = self.db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
        if alert:
            alert.is_resolved = True
            alert.resolved_at = datetime.utcnow()
            alert.resolved_by = user_id
            self.db.commit()
            return True
        return False