import React from 'react';
import { AlertTriangle, Clock, TrendingUp, CreditCard, FileX } from 'lucide-react';
import { RiskAlert } from '../../types';

interface RecentAlertsProps {
  alerts: RiskAlert[];
}

const RecentAlerts: React.FC<RecentAlertsProps> = ({ alerts }) => {
  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'pd-increase':
        return TrendingUp;
      case 'credit-limit':
        return CreditCard;
      case 'payment-delay':
        return Clock;
      case 'financial-deterioration':
        return FileX;
      default:
        return AlertTriangle;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'high':
        return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('tr-TR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">Son Uyarılar</h3>
      
      <div className="space-y-4">
        {alerts.slice(0, 5).map((alert) => {
          const Icon = getAlertIcon(alert.type);
          
          return (
            <div key={alert.id} className={`flex items-start space-x-4 p-4 rounded-lg border ${!alert.isRead ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200'}`}>
              <div className={`p-2 rounded-lg ${getSeverityColor(alert.severity)}`}>
                <Icon className="h-5 w-5" />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{alert.companyName}</p>
                    <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                  </div>
                  {!alert.isRead && (
                    <div className="ml-2">
                      <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    </div>
                  )}
                </div>
                
                <p className="text-xs text-gray-500 mt-2">{formatDate(alert.createdAt)}</p>
              </div>
            </div>
          );
        })}
        
        {alerts.length === 0 && (
          <div className="text-center py-8">
            <AlertTriangle className="h-12 w-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">Henüz uyarı bulunmuyor</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecentAlerts;