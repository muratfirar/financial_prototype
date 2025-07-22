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
  tax_id: string;
  tax_office?: string;
  trade_registry_no?: string;
  mersis_no?: string;
  company_type?: string;
  establishment_date?: string;
  phone?: string;
  email?: string;
  website?: string;
  address?: string;
  city?: string;
  district?: string;
  contact_person?: string;
  contact_phone?: string;
  contact_email?: string;
  sector: string;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  credit_limit: number;
  last_analysis: string;
  pd_score: number; // Probability of Default
  financial_health: 'excellent' | 'good' | 'average' | 'poor' | 'critical';
  revenue: number;
  assets: number;
  liabilities: number;
  status: 'active' | 'inactive' | 'monitoring';
  created_at: string;
  updated_at?: string;
  created_by: number;
  
  // Computed properties for backward compatibility
  get taxId(): string { return this.tax_id; }
  get riskScore(): number { return this.risk_score; }
  get riskLevel(): 'low' | 'medium' | 'high' | 'critical' { return this.risk_level; }
  get creditLimit(): number { return this.credit_limit; }
  get lastAnalysis(): string { return this.last_analysis; }
  get pdScore(): number { return this.pd_score; }
  get financialHealth(): 'excellent' | 'good' | 'average' | 'poor' | 'critical' { return this.financial_health; }
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