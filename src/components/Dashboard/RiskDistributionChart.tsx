import React from 'react';
import { Company } from '../../types';

interface RiskDistributionChartProps {
  companies: Company[];
}

const RiskDistributionChart: React.FC<RiskDistributionChartProps> = ({ companies }) => {
  const riskLevels = companies.reduce((acc, company) => {
    acc[company.riskLevel] = (acc[company.riskLevel] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const total = companies.length;
  const data = [
    { level: 'Düşük', count: riskLevels.low || 0, color: 'bg-green-500', percentage: ((riskLevels.low || 0) / total) * 100 },
    { level: 'Orta', count: riskLevels.medium || 0, color: 'bg-yellow-500', percentage: ((riskLevels.medium || 0) / total) * 100 },
    { level: 'Yüksek', count: riskLevels.high || 0, color: 'bg-orange-500', percentage: ((riskLevels.high || 0) / total) * 100 },
    { level: 'Kritik', count: riskLevels.critical || 0, color: 'bg-red-500', percentage: ((riskLevels.critical || 0) / total) * 100 }
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">Risk Dağılımı</h3>
      
      <div className="space-y-4">
        {data.map((item, index) => (
          <div key={index} className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className={`w-4 h-4 rounded ${item.color}`}></div>
              <span className="text-sm font-medium text-gray-700">{item.level} Risk</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex-1 max-w-32">
                <div className="bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${item.color}`}
                    style={{ width: `${item.percentage}%` }}
                  ></div>
                </div>
              </div>
              <span className="text-sm font-semibold text-gray-900 w-8">{item.count}</span>
              <span className="text-sm text-gray-500 w-12">{item.percentage.toFixed(1)}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RiskDistributionChart;