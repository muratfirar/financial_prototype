import React, { useState } from 'react';
import { Shield, TrendingUp, AlertTriangle, Calculator, FileText, BarChart } from 'lucide-react';
import { companies } from '../../data/mockData';

const RiskAnalysis: React.FC = () => {
  const [selectedCompany, setSelectedCompany] = useState('');
  const [analysisType, setAnalysisType] = useState<'credit' | 'pd' | 'stress'>('credit');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalysis = async () => {
    setIsAnalyzing(true);
    // Simulate analysis process
    await new Promise(resolve => setTimeout(resolve, 3000));
    setIsAnalyzing(false);
  };

  const selectedCompanyData = companies.find(c => c.id === selectedCompany);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-3 mb-6">
          <Shield className="h-6 w-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">Risk Analizi</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Firma Seçimi</label>
            <select
              value={selectedCompany}
              onChange={(e) => setSelectedCompany(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Firma seçiniz...</option>
              {companies.map(company => (
                <option key={company.id} value={company.id}>{company.name}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Analiz Türü</label>
            <select
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value as 'credit' | 'pd' | 'stress')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="credit">Kredi Risk Analizi</option>
              <option value="pd">PD (Temerrüt) Analizi</option>
              <option value="stress">Stres Test Analizi</option>
            </select>
          </div>
          
          <div className="flex items-end">
            <button
              onClick={handleAnalysis}
              disabled={!selectedCompany || isAnalyzing}
              className={`w-full px-4 py-2 rounded-lg font-medium ${
                selectedCompany && !isAnalyzing
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {isAnalyzing ? 'Analiz Ediliyor...' : 'Analizi Başlat'}
            </button>
          </div>
        </div>
      </div>
      
      {selectedCompanyData && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Mevcut Risk Profili</h3>
              <Calculator className="h-6 w-6 text-blue-600" />
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Risk Skoru</p>
                  <p className="text-sm text-gray-600">0-1000 arası</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-blue-600">{selectedCompanyData.riskScore}</p>
                  <p className="text-sm text-blue-600">
                    {selectedCompanyData.riskLevel === 'low' ? 'Düşük Risk' :
                     selectedCompanyData.riskLevel === 'medium' ? 'Orta Risk' :
                     selectedCompanyData.riskLevel === 'high' ? 'Yüksek Risk' : 'Kritik Risk'}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-orange-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">PD Skoru</p>
                  <p className="text-sm text-gray-600">Temerrüt olasılığı (%)</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-orange-600">{selectedCompanyData.pdScore}%</p>
                  <p className="text-sm text-orange-600">
                    {selectedCompanyData.pdScore < 5 ? 'Düşük' :
                     selectedCompanyData.pdScore < 10 ? 'Orta' : 'Yüksek'}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Kredi Limiti</p>
                  <p className="text-sm text-gray-600">Önerilen maksimum</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-600">
                    {new Intl.NumberFormat('tr-TR', {
                      style: 'currency',
                      currency: 'TRY',
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0
                    }).format(selectedCompanyData.creditLimit)}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Risk Faktörleri</h3>
              <BarChart className="h-6 w-6 text-orange-600" />
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Finansal Sağlık</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        selectedCompanyData.financialHealth === 'excellent' ? 'bg-green-500 w-full' :
                        selectedCompanyData.financialHealth === 'good' ? 'bg-blue-500 w-4/5' :
                        selectedCompanyData.financialHealth === 'average' ? 'bg-yellow-500 w-3/5' :
                        selectedCompanyData.financialHealth === 'poor' ? 'bg-orange-500 w-2/5' :
                        'bg-red-500 w-1/5'
                      }`}
                    ></div>
                  </div>
                  <span className="text-sm font-medium">
                    {selectedCompanyData.financialHealth === 'excellent' ? 'Mükemmel' :
                     selectedCompanyData.financialHealth === 'good' ? 'İyi' :
                     selectedCompanyData.financialHealth === 'average' ? 'Orta' :
                     selectedCompanyData.financialHealth === 'poor' ? 'Zayıf' : 'Kritik'}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Sektör Riski</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="h-2 rounded-full bg-blue-500 w-3/5"></div>
                  </div>
                  <span className="text-sm font-medium">Orta</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Ödeme Geçmişi</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="h-2 rounded-full bg-green-500 w-full"></div>
                  </div>
                  <span className="text-sm font-medium">İyi</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Makroekonomik</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="h-2 rounded-full bg-yellow-500 w-2/5"></div>
                  </div>
                  <span className="text-sm font-medium">Düşük</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Likidite Durumu</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className={`h-2 rounded-full ${
                      selectedCompanyData.assets > selectedCompanyData.liabilities * 1.5 ? 'bg-green-500 w-4/5' :
                      selectedCompanyData.assets > selectedCompanyData.liabilities ? 'bg-yellow-500 w-3/5' :
                      'bg-red-500 w-2/5'
                    }`}></div>
                  </div>
                  <span className="text-sm font-medium">
                    {selectedCompanyData.assets > selectedCompanyData.liabilities * 1.5 ? 'İyi' :
                     selectedCompanyData.assets > selectedCompanyData.liabilities ? 'Orta' : 'Zayıf'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {isAnalyzing && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {analysisType === 'credit' ? 'Kredi Risk Analizi' :
               analysisType === 'pd' ? 'PD Analizi' : 'Stres Test Analizi'} Yapılıyor
            </h3>
            <p className="text-gray-600">
              Finansal veriler analiz ediliyor ve risk modelleri hesaplanıyor...
            </p>
          </div>
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Kredi Risk Analizi</h3>
            <Shield className="h-8 w-8 opacity-80" />
          </div>
          <p className="text-blue-100 mb-4">
            Firmanın kredi riskini kapsamlı analiz edin ve optimal kredi limitini belirleyin.
          </p>
          <div className="flex items-center space-x-2 text-blue-100">
            <Calculator className="h-4 w-4" />
            <span className="text-sm">Risk skoru algoritması</span>
          </div>
        </div>
        
        <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">PD Tahmin Analizi</h3>
            <TrendingUp className="h-8 w-8 opacity-80" />
          </div>
          <p className="text-orange-100 mb-4">
            Makine öğrenmesi algoritmaları ile temerrüt olasılığını tahmin edin.
          </p>
          <div className="flex items-center space-x-2 text-orange-100">
            <BarChart className="h-4 w-4" />
            <span className="text-sm">ML tabanlı tahmin</span>
          </div>
        </div>
        
        <div className="bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Stres Test Analizi</h3>
            <AlertTriangle className="h-8 w-8 opacity-80" />
          </div>
          <p className="text-red-100 mb-4">
            Farklı ekonomik senaryolar altında risk durumunu değerlendirin.
          </p>
          <div className="flex items-center space-x-2 text-red-100">
            <FileText className="h-4 w-4" />
            <span className="text-sm">Senaryo analizi</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskAnalysis;