import React, { useState } from 'react';
import { X, Save, Building2, User, Phone, Mail, MapPin } from 'lucide-react';
import { Company } from '../../types';
import { companiesAPI } from '../../services/api';

interface CompanyFormProps {
  company?: Company;
  onClose: () => void;
  onSave: (company: Company) => void;
}

const CompanyForm: React.FC<CompanyFormProps> = ({ company, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    // Firma Bilgileri
    name: company?.name || '',
    tax_id: company?.tax_id || '',
    tax_office: company?.tax_office || '',
    trade_registry_no: company?.trade_registry_no || '',
    mersis_no: company?.mersis_no || '',
    company_type: company?.company_type || '',
    establishment_date: company?.establishment_date || '',
    
    // İletişim Bilgileri
    phone: company?.phone || '',
    email: company?.email || '',
    website: company?.website || '',
    address: company?.address || '',
    city: company?.city || '',
    district: company?.district || '',
    
    // Yetkili Bilgileri
    contact_person: company?.contact_person || '',
    contact_phone: company?.contact_phone || '',
    contact_email: company?.contact_email || '',
    
    // Finansal Bilgiler
    sector: company?.sector || '',
    revenue: company?.revenue || 0,
    assets: company?.assets || 0,
    liabilities: company?.liabilities || 0,
    credit_limit: company?.creditLimit || 0,
  });

  const [activeTab, setActiveTab] = useState('company');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  // Validation functions
  const validateTaxId = (taxId: string): boolean => {
    // VKN (10 haneli) veya TCKN (11 haneli) kontrolü
    if (taxId.length === 10) {
      return /^[0-9]{10}$/.test(taxId);
    } else if (taxId.length === 11) {
      return /^[1-9][0-9]{10}$/.test(taxId) && validateTCKN(taxId);
    }
    return false;
  };

  const validateTCKN = (tckn: string): boolean => {
    if (tckn.length !== 11) return false;
    
    const digits = tckn.split('').map(Number);
    
    // İlk 10 hanenin toplamı
    const sum1 = digits.slice(0, 10).reduce((a, b) => a + b, 0);
    if (sum1 % 10 !== digits[10]) return false;
    
    // Tek ve çift hanelerin toplamı
    const oddSum = digits[0] + digits[2] + digits[4] + digits[6] + digits[8];
    const evenSum = digits[1] + digits[3] + digits[5] + digits[7];
    
    if (((oddSum * 7) - evenSum) % 10 !== digits[9]) return false;
    
    return true;
  };

  const validateEmail = (email: string): boolean => {
    return /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email);
  };

  const validatePhone = (phone: string): boolean => {
    return /^(\+90|0)?[5][0-9]{9}$/.test(phone.replace(/\s/g, ''));
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    // Zorunlu alanlar
    if (!formData.name.trim()) errors.name = 'Firma ünvanı zorunludur';
    if (!formData.tax_id.trim()) errors.tax_id = 'Vergi numarası zorunludur';
    else if (!validateTaxId(formData.tax_id)) {
      errors.tax_id = 'Geçerli bir VKN (10 haneli) veya TCKN (11 haneli) giriniz';
    }
    if (!formData.tax_office.trim()) errors.tax_office = 'Vergi dairesi zorunludur';
    if (!formData.company_type.trim()) errors.company_type = 'Firma tipi zorunludur';
    if (!formData.phone.trim()) errors.phone = 'Telefon numarası zorunludur';
    else if (!validatePhone(formData.phone)) {
      errors.phone = 'Geçerli bir telefon numarası giriniz (0xxx xxx xx xx)';
    }
    if (!formData.email.trim()) errors.email = 'E-posta adresi zorunludur';
    else if (!validateEmail(formData.email)) {
      errors.email = 'Geçerli bir e-posta adresi giriniz';
    }
    if (!formData.address.trim()) errors.address = 'Adres zorunludur';
    if (!formData.city.trim()) errors.city = 'İl zorunludur';
    if (!formData.district.trim()) errors.district = 'İlçe zorunludur';
    if (!formData.contact_person.trim()) errors.contact_person = 'Yetkili adı zorunludur';
    if (!formData.contact_phone.trim()) errors.contact_phone = 'Yetkili telefonu zorunludur';
    else if (!validatePhone(formData.contact_phone)) {
      errors.contact_phone = 'Geçerli bir telefon numarası giriniz';
    }
    if (!formData.contact_email.trim()) errors.contact_email = 'Yetkili e-postası zorunludur';
    else if (!validateEmail(formData.contact_email)) {
      errors.contact_email = 'Geçerli bir e-posta adresi giriniz';
    }
    if (!formData.sector.trim()) errors.sector = 'Sektör zorunludur';

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      setError('Lütfen tüm zorunlu alanları doğru şekilde doldurunuz.');
      return;
    }

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
    
    // Clear validation error when user starts typing
    if (validationErrors[name]) {
      setValidationErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const companyTypes = [
    'A.Ş.', 'Ltd. Şti.', 'Koll. Şti.', 'Kom. Şti.', 'Adi Şirket', 
    'San. ve Tic. A.Ş.', 'San. ve Tic. Ltd. Şti.', 'Şahıs Firması'
  ];

  const sectors = [
    'Teknoloji', 'Gıda', 'Tekstil', 'İnşaat', 'Otomotiv', 
    'Enerji', 'Turizm', 'Havacılık', 'Sağlık', 'Eğitim',
    'Finans', 'Perakende', 'Lojistik', 'İmalat', 'Tarım'
  ];

  const cities = [
    'İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana',
    'Konya', 'Gaziantep', 'Mersin', 'Diyarbakır', 'Kayseri', 'Eskişehir'
  ];

  const tabs = [
    { id: 'company', label: 'Firma Bilgileri', icon: Building2 },
    { id: 'contact', label: 'İletişim Bilgileri', icon: MapPin },
    { id: 'person', label: 'Yetkili Bilgileri', icon: User },
    { id: 'financial', label: 'Finansal Bilgiler', icon: Save }
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
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

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          {/* Firma Bilgileri Tab */}
          {activeTab === 'company' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Firma Ünvanı *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.name ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  />
                  {validationErrors.name && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.name}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Vergi Numarası (VKN/TCKN) *
                  </label>
                  <input
                    type="text"
                    name="tax_id"
                    value={formData.tax_id}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.tax_id ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="10 haneli VKN veya 11 haneli TCKN"
                    required
                  />
                  {validationErrors.tax_id && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.tax_id}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Vergi Dairesi *
                  </label>
                  <input
                    type="text"
                    name="tax_office"
                    value={formData.tax_office}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.tax_office ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  />
                  {validationErrors.tax_office && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.tax_office}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Firma Tipi *
                  </label>
                  <select
                    name="company_type"
                    value={formData.company_type}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.company_type ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  >
                    <option value="">Firma tipi seçiniz</option>
                    {companyTypes.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                  {validationErrors.company_type && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.company_type}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Ticaret Sicil No
                  </label>
                  <input
                    type="text"
                    name="trade_registry_no"
                    value={formData.trade_registry_no}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Mersis No
                  </label>
                  <input
                    type="text"
                    name="mersis_no"
                    value={formData.mersis_no}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Kuruluş Tarihi
                  </label>
                  <input
                    type="date"
                    name="establishment_date"
                    value={formData.establishment_date}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.sector ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  >
                    <option value="">Sektör seçiniz</option>
                    {sectors.map(sector => (
                      <option key={sector} value={sector}>{sector}</option>
                    ))}
                  </select>
                  {validationErrors.sector && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.sector}</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* İletişim Bilgileri Tab */}
          {activeTab === 'contact' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Telefon Numarası *
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.phone ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="0xxx xxx xx xx"
                    required
                  />
                  {validationErrors.phone && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.phone}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    E-posta Adresi *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.email ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  />
                  {validationErrors.email && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.email}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Web Sitesi
                  </label>
                  <input
                    type="url"
                    name="website"
                    value={formData.website}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="https://www.example.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    İl *
                  </label>
                  <select
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.city ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  >
                    <option value="">İl seçiniz</option>
                    {cities.map(city => (
                      <option key={city} value={city}>{city}</option>
                    ))}
                  </select>
                  {validationErrors.city && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.city}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    İlçe *
                  </label>
                  <input
                    type="text"
                    name="district"
                    value={formData.district}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.district ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  />
                  {validationErrors.district && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.district}</p>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Adres *
                </label>
                <textarea
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  rows={3}
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    validationErrors.address ? 'border-red-500' : 'border-gray-300'
                  }`}
                  required
                />
                {validationErrors.address && (
                  <p className="text-red-500 text-sm mt-1">{validationErrors.address}</p>
                )}
              </div>
            </div>
          )}

          {/* Yetkili Bilgileri Tab */}
          {activeTab === 'person' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Adı Soyadı *
                  </label>
                  <input
                    type="text"
                    name="contact_person"
                    value={formData.contact_person}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.contact_person ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  />
                  {validationErrors.contact_person && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.contact_person}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Cep Telefonu *
                  </label>
                  <input
                    type="tel"
                    name="contact_phone"
                    value={formData.contact_phone}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.contact_phone ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="0xxx xxx xx xx"
                    required
                  />
                  {validationErrors.contact_phone && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.contact_phone}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    E-posta *
                  </label>
                  <input
                    type="email"
                    name="contact_email"
                    value={formData.contact_email}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      validationErrors.contact_email ? 'border-red-500' : 'border-gray-300'
                    }`}
                    required
                  />
                  {validationErrors.contact_email && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.contact_email}</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Finansal Bilgiler Tab */}
          {activeTab === 'financial' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          <div className="flex items-center justify-between pt-6 border-t border-gray-200">
            <div className="flex space-x-2">
              {activeTab !== 'company' && (
                <button
                  type="button"
                  onClick={() => {
                    const currentIndex = tabs.findIndex(tab => tab.id === activeTab);
                    if (currentIndex > 0) {
                      setActiveTab(tabs[currentIndex - 1].id);
                    }
                  }}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Önceki
                </button>
              )}
              
              {activeTab !== 'financial' && (
                <button
                  type="button"
                  onClick={() => {
                    const currentIndex = tabs.findIndex(tab => tab.id === activeTab);
                    if (currentIndex < tabs.length - 1) {
                      setActiveTab(tabs[currentIndex + 1].id);
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Sonraki
                </button>
              )}
            </div>

            <div className="flex space-x-4">
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
          </div>
        </form>
      </div>
    </div>
  );
};

export default CompanyForm;