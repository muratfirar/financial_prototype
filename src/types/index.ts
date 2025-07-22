export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'manager' | 'risk-analyst' | 'data-observer' | 'dealer';
  avatar?: string;
  lastActive: string;
}

export interface Company {
  id: string;
  name: string;
  taxId: string;
  sector: string;
  riskScore: number;
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  creditLimit: number;
  lastAnalysis: string;
  pdScore: number; // Probability of Default
  financialHealth: 'excellent' | 'good' | 'average' | 'poor' | 'critical';
  revenue: number;
  assets: number;
  liabilities: number;
  status: 'active' | 'inactive' | 'monitoring';
}

export interface RiskAlert {
  id: string;
  companyId: string;
  companyName: string;
  type: 'credit-limit' | 'pd-increase' | 'payment-delay' | 'financial-deterioration';
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  createdAt: string;
  isRead: boolean;
}

export interface FinancialMetric {
  id: string;
  companyId: string;
  period: string;
  revenue: number;
  netIncome: number;
  totalAssets: number;
  totalLiabilities: number;
  cashFlow: number;
  debtToEquity: number;
  currentRatio: number;
  quickRatio: number;
  createdAt: string;
}