import React from 'react';
import { ArrowLeft, Building2, TrendingUp, TrendingDown, AlertTriangle, Shield, DollarSign } from 'lucide-react';
import { Company } from '../../types';

interface CompanyDetailProps {
  company: Company;
  onBack: () => void;
}

const CompanyDetail: React.FC<CompanyDetailProps> = ({ company, onBack }) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'low':
        return 'text-green-600 bg-green-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'high':
        return 'text-orange-600 bg-orange-100';
      case 'critical':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'excellent':
        return 'text-green-600 bg-green-100';
      case 'good':
        return 'text-blue-600 bg-blue-100';
      case 'average':
        return 'text-yellow-600 bg-yellow-100';
      case 'poor':
        return 'text-orange-600 bg-orange-100';
      case 'critical':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const equity = company.assets - company.liabilities;
  const debtToEquity = equity > 0 ? (company.liabilities / equity).toFixed(2) : 'N/A';

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <button 
            onClick={onBack}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="h-5 w-5" />
            <span>Geri</span>
          </button>
          
          <div className="flex items-center space-x-3">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Risk Analizi Yap
            </button>
            <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
              Rapor Oluştur
            </button>
          </div>
        </div>
        
        <div className="flex items-start space-x-6">
          <div className="flex-1">
            <div className="flex items-center space-x-4 mb-4">
              <div className="p-3 bg-blue-100 rounded-lg">
                <Building2 className="h-8 w-8 text-blue-600" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{company.name}</h1>
                <p className="text-gray-600">{company.taxId} • {company.sector}</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{company.riskScore}</div>
                <div className="text-sm text-gray-500">Risk Skoru</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{company.pdScore}%</div>
                <div className="text-sm text-gray-500">PD Skoru</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{formatCurrency(company.creditLimit)}</div>
                <div className="text-sm text-gray-500">Kredi Limiti</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{company.lastAnalysis}</div>
                <div className="text-sm text-gray-500">Son Analiz</div>
              </div>
            </div>
          </div>
          
          <div className="space-y-3">
            <div className={`px-4 py-2 rounded-lg text-center ${getRiskColor(company.riskLevel)}`}>
              <div className="font-semibold">
                {company.riskLevel === 'low' ? 'Düşük Risk' : 
                 company.riskLevel === 'medium' ? 'Orta Risk' :
                 company.riskLevel === 'high' ? 'Yüksek Risk' : 'Kritik Risk'}
              </div>
            </div>
            <div className={`px-4 py-2 rounded-lg text-center ${getHealthColor(company.financialHealth)}`}>
              <div className="font-semibold">
                {company.financialHealth === 'excellent' ? 'Mükemmel' :
                 company.financialHealth === 'good' ? 'İyi' :
                 company.financialHealth === 'average' ? 'Orta' :
                 company.financialHealth === 'poor' ? 'Zayıf' : 'Kritik'} Sağlık
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Finansal Özet</h3>
            <DollarSign className="h-6 w-6 text-green-600" />
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Toplam Gelir</span>
              <span className="font-semibold">{formatCurrency(company.revenue)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Toplam Varlık</span>
              <span className="font-semibold">{formatCurrency(company.assets)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Toplam Borç</span>
              <span className="font-semibold">{formatCurrency(company.liabilities)}</span>
            </div>
            <div className="flex justify-between border-t pt-2">
              <span className="text-gray-600">Özkaynak</span>
              <span className={`font-semibold ${equity >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(equity)}
              </span>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Finansal Oranlar</h3>
            <TrendingUp className="h-6 w-6 text-blue-600" />
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Borç/Özkaynak</span>
              <span className="font-semibold">{debtToEquity}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Varlık Getirisi</span>
              <span className="font-semibold">-</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Cari Oran</span>
              <span className="font-semibold">-</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Likidite Oranı</span>
              <span className="font-semibold">-</span>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Risk İndikatörleri</h3>
            <Shield className="h-6 w-6 text-orange-600" />
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Ödeme Gecikmeleri</span>
              <span className="flex items-center space-x-1">
                <span className="font-semibold">0</span>
                {company.riskLevel !== 'low' && <AlertTriangle className="h-4 w-4 text-yellow-500" />}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Sektör Karşılaştırma</span>
              <span className="font-semibold text-green-600">Ortalamanın Üstü</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Trend Analizi</span>
              <span className="flex items-center space-x-1">
                <span className="font-semibold">Pozitif</span>
                <TrendingUp className="h-4 w-4 text-green-500" />
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Makroekonomik Risk</span>
              <span className="font-semibold">Düşük</span>
            </div>
          </div>
        </div>
      </div>
      
      {showEDefterUpload && (
        <EDefterUpload
          company={company}
          onClose={() => setShowEDefterUpload(false)}
          onUploadSuccess={() => {
            setShowEDefterUpload(false);
            // Refresh company data
            window.location.reload();
          }}
        />
      )}
    </div>
  );
};

export default CompanyDetail;