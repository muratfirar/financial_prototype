import React from 'react';
import { Bell, Search, User, LogOut } from 'lucide-react';
import { User as UserType } from '../../types';

interface HeaderProps {
  user: UserType;
  unreadAlerts: number;
}

const Header: React.FC<HeaderProps> = ({ user, unreadAlerts }) => {
  const getRoleLabel = (role: string) => {
    const roles = {
      'admin': 'Sistem Yöneticisi',
      'manager': 'Yönetici',
      'risk-analyst': 'Risk Analisti',
      'data-observer': 'Veri İzleyicisi',
      'dealer': 'Bayi'
    };
    return roles[role as keyof typeof roles] || role;
  };

  return (
    <div className="bg-white shadow-sm border-b border-gray-200 h-16 fixed top-0 right-0 left-64 z-20">
      <div className="flex items-center justify-between h-full px-6">
        <div className="flex items-center flex-1 max-w-md">
          <div className="relative w-full">
            <Search className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
            <input
              type="text"
              placeholder="Firma ara..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <button className="relative p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
            <Bell className="h-5 w-5" />
            {unreadAlerts > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {unreadAlerts}
              </span>
            )}
          </button>
          
          <div className="flex items-center space-x-3 border-l border-gray-300 pl-4">
            <div className="flex items-center space-x-3">
              {user.avatar ? (
                <img 
                  src={user.avatar} 
                  alt={user.name}
                  className="h-8 w-8 rounded-full object-cover"
                />
              ) : (
                <div className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <User className="h-5 w-5 text-white" />
                </div>
              )}
              <div className="text-sm">
                <p className="font-medium text-gray-900">{user.name}</p>
                <p className="text-gray-500">{getRoleLabel(user.role)}</p>
              </div>
            </div>
            
            <button className="p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;