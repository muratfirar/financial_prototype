import { User, Company, RiskAlert, FinancialMetric } from '../types';

export const currentUser: User = {
  id: '1',
  name: 'Ahmet Yılmaz',
  email: 'ahmet.yilmaz@finansal.com',
  role: 'risk-analyst',
  avatar: 'https://images.pexels.com/photos/2379005/pexels-photo-2379005.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
  lastActive: '2025-01-20T10:30:00Z'
};

export const companies: Company[] = [
  {
    id: '1',
    name: 'ABC Teknoloji A.Ş.',
    taxId: '1234567890',
    sector: 'Teknoloji',
    riskScore: 750,
    riskLevel: 'low',
    creditLimit: 5000000,
    lastAnalysis: '2025-01-19',
    pdScore: 2.3,
    financialHealth: 'good',
    revenue: 25000000,
    assets: 15000000,
    liabilities: 8000000,
    status: 'active'
  },
  {
    id: '2',
    name: 'DEF İnşaat Ltd.',
    taxId: '2345678901',
    sector: 'İnşaat',
    riskScore: 520,
    riskLevel: 'high',
    creditLimit: 2000000,
    lastAnalysis: '2025-01-18',
    pdScore: 8.7,
    financialHealth: 'poor',
    revenue: 12000000,
    assets: 20000000,
    liabilities: 18000000,
    status: 'monitoring'
  },
  {
    id: '3',
    name: 'GHI Tekstil San.',
    taxId: '3456789012',
    sector: 'Tekstil',
    riskScore: 680,
    riskLevel: 'medium',
    creditLimit: 3500000,
    lastAnalysis: '2025-01-20',
    pdScore: 4.2,
    financialHealth: 'average',
    revenue: 18000000,
    assets: 12000000,
    liabilities: 7500000,
    status: 'active'
  },
  {
    id: '4',
    name: 'JKL Gıda A.Ş.',
    taxId: '4567890123',
    sector: 'Gıda',
    riskScore: 820,
    riskLevel: 'low',
    creditLimit: 8000000,
    lastAnalysis: '2025-01-19',
    pdScore: 1.8,
    financialHealth: 'excellent',
    revenue: 45000000,
    assets: 30000000,
    liabilities: 12000000,
    status: 'active'
  },
  {
    id: '5',
    name: 'MNO Otomotiv Ltd.',
    taxId: '5678901234',
    sector: 'Otomotiv',
    riskScore: 420,
    riskLevel: 'critical',
    creditLimit: 1000000,
    lastAnalysis: '2025-01-20',
    pdScore: 15.2,
    financialHealth: 'critical',
    revenue: 8000000,
    assets: 15000000,
    liabilities: 16500000,
    status: 'monitoring'
  }
];

export const riskAlerts: RiskAlert[] = [
  {
    id: '1',
    companyId: '2',
    companyName: 'DEF İnşaat Ltd.',
    type: 'pd-increase',
    severity: 'high',
    message: 'PD skoru son 30 günde %25 artış gösterdi',
    createdAt: '2025-01-20T09:15:00Z',
    isRead: false
  },
  {
    id: '2',
    companyId: '5',
    companyName: 'MNO Otomotiv Ltd.',
    type: 'financial-deterioration',
    severity: 'critical',
    message: 'Finansal sağlık durumu kritik seviyeye düştü',
    createdAt: '2025-01-20T08:30:00Z',
    isRead: false
  },
  {
    id: '3',
    companyId: '3',
    companyName: 'GHI Tekstil San.',
    type: 'credit-limit',
    severity: 'medium',
    message: 'Kredi kullanım oranı %80\'i geçti',
    createdAt: '2025-01-19T16:45:00Z',
    isRead: true
  }
];

export const dashboardStats = {
  totalCompanies: companies.length,
  activeAnalyses: 12,
  criticalAlerts: riskAlerts.filter(alert => alert.severity === 'critical' && !alert.isRead).length,
  averageRiskScore: Math.round(companies.reduce((sum, company) => sum + company.riskScore, 0) / companies.length),
  totalCreditExposure: companies.reduce((sum, company) => sum + company.creditLimit, 0),
  highRiskCompanies: companies.filter(company => company.riskLevel === 'high' || company.riskLevel === 'critical').length
};