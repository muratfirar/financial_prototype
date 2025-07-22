import React, { useState } from 'react';
import { X, Save, Building2 } from 'lucide-react';
import { Company } from '../../types';
import { companiesAPI } from '../../services/api';

interface CompanyFormProps {
  company?: Company;
  onClose: () => void;
  onSave: (company: Company) => void;
}

const CompanyForm: React.FC<CompanyFormProps> = ({ company, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    name: company?.name || '',
    tax_id: company?.taxId || '',
    sector: company?.sector || '',
    revenue: company?.revenue || 0,
    assets: company?.assets || 0,
    liabilities: company?.liabilities || 0,
    credit_limit: company?.creditLimit || 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      let result;
      if (company) {
        result = await companiesAPI.update(company.id, formData);
      } else {
        result = await companiesAPI.create(formData);
      }
      onSave(result);
      onClose();
    } catch (err) {
      setError('Firma kaydedilirken bir hata oluştu.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name.includes('revenue') || name.includes('assets') || name.includes('liabilities') || name.includes('credit_limit')
        ? parseFloat(value) || 0
        : value
    }));
  };

  const sectors = [
    'Teknoloji', 'Gıda', 'Tekstil', 'İnşaat', 'Otomotiv', 
    'Enerji', 'Turizm', 'Havacılık', 'Sağlık', 'Eğitim'
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <Building2 className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              {company ? 'Firma Düzenle' : 'Yeni Firma Ekle'}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Firma Adı *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Vergi Numarası *
              </label>
              <input
                type="text"
                name="tax_id"
                value={formData.tax_id}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sektör *
              </label>
              <select
                name="sector"
                value={formData.sector}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Sektör seçiniz</option>
                {sectors.map(sector => (
                  <option key={sector} value={sector}>{sector}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Yıllık Gelir (TL)
              </label>
              <input
                type="number"
                name="revenue"
                value={formData.revenue}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                min="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Toplam Varlık (TL)
              </label>
              <input
                type="number"
                name="assets"
                value={formData.assets}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                min="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Toplam Borç (TL)
              </label>
              <input
                type="number"
                name="liabilities"
                value={formData.liabilities}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                min="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Kredi Limiti (TL)
              </label>
              <input
                type="number"
                name="credit_limit"
                value={formData.credit_limit}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                min="0"
              />
            </div>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          <div className="flex items-center justify-end space-x-4 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              İptal
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium ${
                isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              <Save className="h-4 w-4" />
              <span>{isLoading ? 'Kaydediliyor...' : 'Kaydet'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CompanyForm;