import pytest
from app.services.risk_engine import RiskEngine
from app.models.company import Company, RiskLevel, FinancialHealth, CompanyStatus
from app.models.financial_metric import FinancialMetric

class TestRiskEngine:
    
    def setup_method(self):
        self.risk_engine = RiskEngine()
        
        # Create a sample company for testing
        self.sample_company = Company(
            id=1,
            name="Test Company",
            tax_id="1234567890",
            sector="Teknoloji",
            revenue=10000000,
            assets=8000000,
            liabilities=3000000,
            credit_limit=2000000,
            risk_score=650,
            risk_level=RiskLevel.MEDIUM,
            pd_score=5.0,
            financial_health=FinancialHealth.AVERAGE,
            status=CompanyStatus.ACTIVE,
            created_by=1
        )
        
        # Create sample financial metrics
        self.sample_metrics = FinancialMetric(
            id=1,
            company_id=1,
            period="2024-Q4",
            revenue=2500000,  # Quarterly
            net_income=250000,
            total_assets=8000000,
            total_liabilities=3000000,
            equity=5000000,
            debt_to_equity=0.6,
            current_ratio=1.5,
            quick_ratio=1.2,
            roa=3.1,  # 250k / 8M * 100
            roe=5.0   # 250k / 5M * 100
        )
    
    def test_calculate_credit_score_basic(self):
        """Test basic credit score calculation"""
        score = self.risk_engine.calculate_credit_score(self.sample_company)
        
        assert isinstance(score, int)
        assert 0 <= score <= 1000
        assert score > 500  # Should be above base score for healthy company
    
    def test_calculate_credit_score_with_metrics(self):
        """Test credit score calculation with detailed financial metrics"""
        score = self.risk_engine.calculate_credit_score(self.sample_company, self.sample_metrics)
        
        assert isinstance(score, int)
        assert 0 <= score <= 1000
        # Should be higher with good financial metrics
        assert score >= 600
    
    def test_calculate_pd_score_basic(self):
        """Test PD score calculation"""
        pd_score = self.risk_engine.calculate_pd_score(self.sample_company)
        
        assert isinstance(pd_score, float)
        assert 0.1 <= pd_score <= 50.0
    
    def test_calculate_pd_score_with_metrics(self):
        """Test PD score calculation with financial metrics"""
        pd_score = self.risk_engine.calculate_pd_score(self.sample_company, self.sample_metrics)
        
        assert isinstance(pd_score, float)
        assert 0.1 <= pd_score <= 50.0
        # Should be reasonable for a healthy company
        assert pd_score < 10.0
    
    def test_calculate_recommended_credit_limit(self):
        """Test recommended credit limit calculation"""
        limit = self.risk_engine.calculate_recommended_credit_limit(self.sample_company)
        
        assert isinstance(limit, float)
        assert 100000 <= limit <= 50000000  # Within defined bounds
        # Should be reasonable relative to company size
        assert limit <= self.sample_company.assets
    
    def test_sector_risk_adjustment(self):
        """Test that sector risk affects calculations"""
        # Test with high-risk sector
        high_risk_company = Company(
            id=2,
            name="Construction Company",
            tax_id="9876543210",
            sector="İnşaat",  # High risk sector
            revenue=10000000,
            assets=8000000,
            liabilities=3000000,
            credit_limit=2000000,
            risk_score=650,
            risk_level=RiskLevel.MEDIUM,
            pd_score=5.0,
            financial_health=FinancialHealth.AVERAGE,
            status=CompanyStatus.ACTIVE,
            created_by=1
        )
        
        tech_pd = self.risk_engine.calculate_pd_score(self.sample_company)
        construction_pd = self.risk_engine.calculate_pd_score(high_risk_company)
        
        # Construction should have higher PD due to sector risk
        assert construction_pd > tech_pd
    
    def test_generate_risk_factors(self):
        """Test risk factors generation"""
        factors = self.risk_engine.generate_risk_factors(self.sample_company, self.sample_metrics)
        
        assert isinstance(factors, dict)
        assert 'profitability' in factors
        assert 'liquidity' in factors
        assert 'leverage' in factors
        assert 'sector_risk' in factors
        
        # Each factor should have required fields
        for factor_name, factor_data in factors.items():
            assert 'score' in factor_data
            assert 'weight' in factor_data
            assert 'status' in factor_data
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Company with zero assets
        zero_asset_company = Company(
            id=3,
            name="Zero Asset Company",
            tax_id="0000000000",
            sector="Test",
            revenue=0,
            assets=0,
            liabilities=0,
            credit_limit=0,
            risk_score=0,
            risk_level=RiskLevel.CRITICAL,
            pd_score=50.0,
            financial_health=FinancialHealth.CRITICAL,
            status=CompanyStatus.INACTIVE,
            created_by=1
        )
        
        score = self.risk_engine.calculate_credit_score(zero_asset_company)
        pd_score = self.risk_engine.calculate_pd_score(zero_asset_company)
        limit = self.risk_engine.calculate_recommended_credit_limit(zero_asset_company)
        
        # Should handle edge cases gracefully
        assert isinstance(score, int)
        assert isinstance(pd_score, float)
        assert isinstance(limit, float)
        assert 0 <= score <= 1000
        assert 0.1 <= pd_score <= 50.0
        assert limit >= 100000  # Minimum limit
    
    def test_high_performing_company(self):
        """Test calculations for a high-performing company"""
        excellent_company = Company(
            id=4,
            name="Excellent Company",
            tax_id="1111111111",
            sector="Gıda",  # Lower risk sector
            revenue=50000000,
            assets=40000000,
            liabilities=10000000,
            credit_limit=10000000,
            risk_score=850,
            risk_level=RiskLevel.LOW,
            pd_score=1.5,
            financial_health=FinancialHealth.EXCELLENT,
            status=CompanyStatus.ACTIVE,
            created_by=1
        )
        
        excellent_metrics = FinancialMetric(
            id=2,
            company_id=4,
            period="2024-Q4",
            revenue=12500000,  # Quarterly
            net_income=1875000,  # 15% margin
            total_assets=40000000,
            total_liabilities=10000000,
            equity=30000000,
            debt_to_equity=0.33,
            current_ratio=2.5,
            quick_ratio=2.0,
            roa=4.7,
            roe=6.25
        )
        
        score = self.risk_engine.calculate_credit_score(excellent_company, excellent_metrics)
        pd_score = self.risk_engine.calculate_pd_score(excellent_company, excellent_metrics)
        
        # Should have high credit score and low PD
        assert score >= 750
        assert pd_score <= 3.0

if __name__ == "__main__":
    pytest.main([__file__])