import React, { useState } from 'react';
import { Building2, BarChart3, Shield, AlertTriangle, TrendingUp, FileText, Users } from 'lucide-react';

// Components
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import StatsCard from './components/Dashboard/StatsCard';
import RiskDistributionChart from './components/Dashboard/RiskDistributionChart';
import RecentAlerts from './components/Dashboard/RecentAlerts';
import CompanyList from './components/Companies/CompanyList';
import CompanyDetail from './components/Companies/CompanyDetail';
import RiskAnalysis from './components/RiskAnalysis/RiskAnalysis';

// Data
import { currentUser, companies, riskAlerts, dashboardStats } from './data/mockData';
import { Company } from './types';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);

  const unreadAlerts = riskAlerts.filter(alert => !alert.isRead).length;

  const renderContent = () => {
    if (selectedCompany && activeSection === 'companies') {
      return (
        <CompanyDetail 
          company={selectedCompany} 
          onBack={() => setSelectedCompany(null)} 
        />
      );
    }

    switch (activeSection) {
      case 'dashboard':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-gray-600">Finansal risk yönetimi platformuna hoş geldiniz</p>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-500">Son güncelleme: Bugün, 10:30</div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatsCard
                title="Toplam Firma"
                value={dashboardStats.totalCompanies}
                icon={Building2}
                color="blue"
                trend={{ value: 12, isPositive: true }}
              />
              <StatsCard
                title="Aktif Analiz"
                value={dashboardStats.activeAnalyses}
                icon={BarChart3}
                color="green"
                trend={{ value: 8, isPositive: true }}
              />
              <StatsCard
                title="Kritik Uyarı"
                value={dashboardStats.criticalAlerts}
                icon={AlertTriangle}
                color="red"
                trend={{ value: -15, isPositive: false }}
              />
              <StatsCard
                title="Ortalama Risk Skoru"
                value={dashboardStats.averageRiskScore}
                icon={Shield}
                color="yellow"
                trend={{ value: 3, isPositive: true }}
              />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <RiskDistributionChart companies={companies} />
              <RecentAlerts alerts={riskAlerts} />
            </div>
            
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Hızlı İşlemler</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => setActiveSection('companies')}
                  className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <Building2 className="h-6 w-6 text-blue-600" />
                  <div className="text-left">
                    <div className="font-medium text-gray-900">Yeni Firma Ekle</div>
                    <div className="text-sm text-gray-500">Firma bilgilerini kaydet</div>
                  </div>
                </button>
                
                <button
                  onClick={() => setActiveSection('risk-analysis')}
                  className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <Shield className="h-6 w-6 text-orange-600" />
                  <div className="text-left">
                    <div className="font-medium text-gray-900">Risk Analizi Yap</div>
                    <div className="text-sm text-gray-500">Detaylı risk değerlendirmesi</div>
                  </div>
                </button>
                
                <button
                  onClick={() => setActiveSection('reports')}
                  className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <FileText className="h-6 w-6 text-green-600" />
                  <div className="text-left">
                    <div className="font-medium text-gray-900">Rapor Oluştur</div>
                    <div className="text-sm text-gray-500">Özel raporlar hazırla</div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        );
        
      case 'companies':
        return (
          <CompanyList 
            companies={companies} 
            onCompanySelect={setSelectedCompany}
          />
        );
        
      case 'risk-analysis':
        return <RiskAnalysis />;
        
      case 'data-integration':
        return (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <TrendingUp className="h-16 w-16 text-blue-600 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Veri Entegrasyonu</h2>
            <p className="text-gray-600 mb-6">PDF, e-defter ve diğer kaynaklardan veri yükleme modülü</p>
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Yakında Gelecek
            </button>
          </div>
        );
        
      case 'early-warning':
        return (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <AlertTriangle className="h-16 w-16 text-orange-600 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Erken Uyarı Sistemi</h2>
            <p className="text-gray-600 mb-6">Otomatik risk tespit ve uyarı modülü</p>
            <button className="px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700">
              Yakında Gelecek
            </button>
          </div>
        );
        
      case 'reports':
        return (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <FileText className="h-16 w-16 text-green-600 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Raporlama Modülü</h2>
            <p className="text-gray-600 mb-6">Özelleştirilebilir raporlar ve dashboard</p>
            <button className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700">
              Yakında Gelecek
            </button>
          </div>
        );
        
      case 'users':
        return (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <Users className="h-16 w-16 text-purple-600 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Kullanıcı Yönetimi</h2>
            <p className="text-gray-600 mb-6">Kullanıcı rolleri ve yetkilendirme</p>
            <button className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
              Yakında Gelecek
            </button>
          </div>
        );
        
      default:
        return (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Bu Modül Geliştiriliyor</h2>
            <p className="text-gray-600">Seçili modül yakında kullanıma sunulacak</p>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar 
        activeSection={activeSection} 
        onSectionChange={setActiveSection}
        userRole={currentUser.role}
      />
      
      <Header user={currentUser} unreadAlerts={unreadAlerts} />
      
      <main className="ml-64 pt-16 p-6">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;