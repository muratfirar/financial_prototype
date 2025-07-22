import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from app.models.company import Company
from app.models.financial_metric import FinancialMetric

class RiskEngine:
    """
    Advanced risk calculation engine for financial risk assessment
    """
    
    def __init__(self):
        self.risk_weights = {
            'financial_health': 0.35,
            'payment_history': 0.25,
            'sector_risk': 0.15,
            'macro_economic': 0.10,
            'liquidity': 0.15
        }
        
        self.sector_risk_multipliers = {
            'Teknoloji': 0.8,
            'Gıda': 0.9,
            'Tekstil': 1.1,
            'İnşaat': 1.3,
            'Otomotiv': 1.2,
            'Enerji': 1.4,
            'Turizm': 1.5,
            'Havacılık': 1.6
        }
    
    def calculate_credit_score(self, company: Company, financial_metrics: Optional[FinancialMetric] = None) -> int:
        """
        Calculate comprehensive credit score (0-1000)
        """
        base_score = 500
        
        # Financial Health Score (0-350 points)
        financial_score = self._calculate_financial_health_score(company, financial_metrics)
        
        # Payment History Score (0-250 points)
        payment_score = self._calculate_payment_history_score(company)
        
        # Sector Risk Score (0-150 points)
        sector_score = self._calculate_sector_risk_score(company)
        
        # Macro Economic Score (0-100 points)
        macro_score = self._calculate_macro_economic_score()
        
        # Liquidity Score (0-150 points)
        liquidity_score = self._calculate_liquidity_score(company, financial_metrics)
        
        total_score = int(base_score + financial_score + payment_score + sector_score + macro_score + liquidity_score)
        
        # Ensure score is within bounds
        return max(0, min(1000, total_score))
    
    def calculate_pd_score(self, company: Company, financial_metrics: Optional[FinancialMetric] = None) -> float:
        """
        Calculate Probability of Default (PD) score using logistic regression approach
        """
        # Base PD calculation using financial ratios
        if not financial_metrics:
            # Use company-level data if detailed metrics not available
            debt_to_equity = company.liabilities / max(company.assets - company.liabilities, 1)
            current_ratio = 1.5  # Default assumption
            roa = 0.05  # Default assumption
        else:
            debt_to_equity = financial_metrics.debt_to_equity
            current_ratio = financial_metrics.current_ratio
            roa = financial_metrics.roa
        
        # Logistic regression coefficients (simplified model)
        intercept = -2.5
        debt_coeff = 1.2
        liquidity_coeff = -0.8
        profitability_coeff = -15.0
        
        # Calculate logit
        logit = (intercept + 
                debt_coeff * min(debt_to_equity, 5) +
                liquidity_coeff * min(current_ratio, 3) +
                profitability_coeff * max(roa, -0.2))
        
        # Convert to probability
        pd_probability = 1 / (1 + np.exp(-logit))
        
        # Apply sector adjustment
        sector_multiplier = self.sector_risk_multipliers.get(company.sector, 1.0)
        adjusted_pd = pd_probability * sector_multiplier
        
        # Convert to percentage and cap at reasonable limits
        return max(0.1, min(50.0, adjusted_pd * 100))
    
    def calculate_recommended_credit_limit(self, company: Company, financial_metrics: Optional[FinancialMetric] = None) -> float:
        """
        Calculate recommended credit limit based on risk assessment
        """
        # Base calculation on company assets and revenue
        asset_based_limit = company.assets * 0.1  # 10% of assets
        revenue_based_limit = company.revenue * 0.2  # 20% of annual revenue
        
        # Take the lower of the two
        base_limit = min(asset_based_limit, revenue_based_limit)
        
        # Apply risk adjustment
        credit_score = self.calculate_credit_score(company, financial_metrics)
        risk_multiplier = self._get_risk_multiplier(credit_score)
        
        recommended_limit = base_limit * risk_multiplier
        
        # Apply sector-specific limits
        sector_multiplier = self.sector_risk_multipliers.get(company.sector, 1.0)
        final_limit = recommended_limit / sector_multiplier
        
        return max(100000, min(50000000, final_limit))  # Min 100K, Max 50M TL
    
    def _calculate_financial_health_score(self, company: Company, financial_metrics: Optional[FinancialMetric]) -> float:
        """Calculate financial health component of credit score"""
        if not financial_metrics:
            # Basic calculation using company data
            equity = company.assets - company.liabilities
            if company.assets > 0:
                equity_ratio = equity / company.assets
                return min(350, equity_ratio * 400)
            return 0
        
        # Detailed calculation using financial metrics
        score = 0
        
        # Profitability (40% of financial health)
        if financial_metrics.revenue > 0:
            profit_margin = financial_metrics.net_income / financial_metrics.revenue
            score += min(140, max(-70, profit_margin * 1000))
        
        # Liquidity (30% of financial health)
        if financial_metrics.current_ratio > 0:
            liquidity_score = min(105, financial_metrics.current_ratio * 50)
            score += liquidity_score
        
        # Leverage (30% of financial health)
        if financial_metrics.debt_to_equity >= 0:
            leverage_score = max(0, 105 - financial_metrics.debt_to_equity * 20)
            score += leverage_score
        
        return max(0, min(350, score))
    
    def _calculate_payment_history_score(self, company: Company) -> float:
        """Calculate payment history component (simplified)"""
        # In a real implementation, this would analyze payment delays, defaults, etc.
        # For now, use a simplified approach based on company status
        if company.status.value == "active":
            return 200  # Good payment history
        elif company.status.value == "monitoring":
            return 100  # Some payment issues
        else:
            return 50   # Poor payment history
    
    def _calculate_sector_risk_score(self, company: Company) -> float:
        """Calculate sector risk component"""
        sector_multiplier = self.sector_risk_multipliers.get(company.sector, 1.0)
        base_sector_score = 100
        
        # Lower multiplier = lower risk = higher score
        return base_sector_score / sector_multiplier
    
    def _calculate_macro_economic_score(self) -> float:
        """Calculate macro economic component (simplified)"""
        # In a real implementation, this would use economic indicators
        return 80  # Neutral macro environment
    
    def _calculate_liquidity_score(self, company: Company, financial_metrics: Optional[FinancialMetric]) -> float:
        """Calculate liquidity component"""
        if not financial_metrics:
            # Basic liquidity assessment
            if company.assets > company.liabilities * 1.5:
                return 120
            elif company.assets > company.liabilities:
                return 80
            else:
                return 20
        
        # Detailed liquidity calculation
        current_ratio_score = min(75, financial_metrics.current_ratio * 25)
        quick_ratio_score = min(75, financial_metrics.quick_ratio * 30)
        
        return current_ratio_score + quick_ratio_score
    
    def _get_risk_multiplier(self, credit_score: int) -> float:
        """Get risk multiplier based on credit score"""
        if credit_score >= 800:
            return 1.5  # Low risk, higher limit
        elif credit_score >= 650:
            return 1.2  # Medium-low risk
        elif credit_score >= 500:
            return 1.0  # Medium risk
        elif credit_score >= 350:
            return 0.7  # Medium-high risk
        else:
            return 0.4  # High risk, lower limit
    
    def generate_risk_factors(self, company: Company, financial_metrics: Optional[FinancialMetric] = None) -> Dict[str, Any]:
        """Generate detailed risk factor analysis"""
        factors = {}
        
        # Financial Health Factors
        if financial_metrics:
            factors['profitability'] = {
                'score': financial_metrics.net_income / max(financial_metrics.revenue, 1) * 100,
                'weight': 0.25,
                'status': 'good' if financial_metrics.net_income > 0 else 'poor'
            }
            factors['liquidity'] = {
                'score': financial_metrics.current_ratio,
                'weight': 0.20,
                'status': 'good' if financial_metrics.current_ratio > 1.2 else 'poor'
            }
            factors['leverage'] = {
                'score': financial_metrics.debt_to_equity,
                'weight': 0.20,
                'status': 'good' if financial_metrics.debt_to_equity < 2.0 else 'poor'
            }
        
        # Sector Risk
        sector_multiplier = self.sector_risk_multipliers.get(company.sector, 1.0)
        factors['sector_risk'] = {
            'score': 1 / sector_multiplier,
            'weight': 0.15,
            'status': 'good' if sector_multiplier < 1.1 else 'medium' if sector_multiplier < 1.3 else 'poor'
        }
        
        # Company Size (stability factor)
        factors['company_size'] = {
            'score': min(1.0, company.revenue / 10000000),  # Normalize to 10M revenue
            'weight': 0.10,
            'status': 'good' if company.revenue > 5000000 else 'medium'
        }
        
        # Payment History (simplified)
        factors['payment_history'] = {
            'score': 1.0 if company.status.value == "active" else 0.5,
            'weight': 0.10,
            'status': 'good' if company.status.value == "active" else 'poor'
        }
        
        return factors