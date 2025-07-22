import React from 'react';
import { 
  BarChart3, 
  Building2, 
  AlertTriangle, 
  FileText, 
  Settings, 
  Users, 
  Shield,
  Upload,
  TrendingUp,
  Bell
} from 'lucide-react';

interface SidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
  userRole: string;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, onSectionChange, userRole }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3, roles: ['admin', 'manager', 'risk-analyst', 'data-observer', 'dealer'] },
    { id: 'companies', label: 'Firma Yönetimi', icon: Building2, roles: ['admin', 'manager', 'risk-analyst'] },
    { id: 'risk-analysis', label: 'Risk Analizi', icon: Shield, roles: ['admin', 'manager', 'risk-analyst'] },
    { id: 'data-integration', label: 'Veri Entegrasyonu', icon: Upload, roles: ['admin', 'manager', 'risk-analyst'] },
    { id: 'early-warning', label: 'Erken Uyarı', icon: AlertTriangle, roles: ['admin', 'manager', 'risk-analyst', 'data-observer'] },
    { id: 'reports', label: 'Raporlar', icon: FileText, roles: ['admin', 'manager', 'risk-analyst', 'data-observer', 'dealer'] },
    { id: 'analytics', label: 'Analitik', icon: TrendingUp, roles: ['admin', 'manager', 'risk-analyst'] },
    { id: 'alerts', label: 'Uyarılar', icon: Bell, roles: ['admin', 'manager', 'risk-analyst'] },
    { id: 'users', label: 'Kullanıcı Yönetimi', icon: Users, roles: ['admin', 'manager'] },
    { id: 'settings', label: 'Ayarlar', icon: Settings, roles: ['admin'] }
  ];

  const filteredItems = menuItems.filter(item => item.roles.includes(userRole));

  return (
    <div className="bg-slate-800 h-full w-64 fixed left-0 top-0 z-10 overflow-y-auto">
      <div className="p-6">
        <div className="flex items-center mb-8">
          <Shield className="h-8 w-8 text-blue-500 mr-3" />
          <div>
            <h1 className="text-white font-bold text-lg">FinRisk</h1>
            <p className="text-slate-400 text-sm">Risk Yönetimi</p>
          </div>
        </div>
        
        <nav>
          {filteredItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => onSectionChange(item.id)}
                className={`flex items-center w-full px-4 py-3 mb-2 text-left rounded-lg transition-all duration-200 ${
                  activeSection === item.id
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                }`}
              >
                <Icon className="h-5 w-5 mr-3" />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;