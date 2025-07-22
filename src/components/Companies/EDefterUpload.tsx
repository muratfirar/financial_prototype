import React, { useState } from 'react';
import { Upload, FileText, Download, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { Company } from '../../types';

interface EDefterUploadProps {
  company: Company;
  onClose: () => void;
  onUploadSuccess: () => void;
}

const EDefterUpload: React.FC<EDefterUploadProps> = ({ company, onClose, onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [period, setPeriod] = useState('2024-12');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [history, setHistory] = useState<any[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Lütfen bir dosya seçin');
      return;
    }

    setIsUploading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch(
        `http://localhost:8000/api/v1/edefter/upload?company_id=${company.id}&period=${period}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
          },
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();
      setUploadResult(result);
      onUploadSuccess();
    } catch (err) {
      setError('Dosya yükleme başarısız oldu');
    } finally {
      setIsUploading(false);
    }
  };

  const downloadSample = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/edefter/download-sample/${company.id}?period=${period}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
          },
        }
      );

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `edefter_${company.tax_id}_${period}.xml`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (err) {
      setError('Örnek dosya indirilemedi');
    }
  };

  const loadHistory = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/edefter/history/${company.id}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setHistory(data);
        setShowHistory(true);
      }
    } catch (err) {
      setError('Geçmiş veriler yüklenemedi');
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <FileText className="h-6 w-6 text-blue-600" />
            <div>
              <h2 className="text-xl font-semibold text-gray-900">e-Defter Yükleme</h2>
              <p className="text-sm text-gray-600">{company.name}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
          >
            ×
          </button>
        </div>

        <div className="p-6">
          {!uploadResult ? (
            <div className="space-y-6">
              {/* Dönem Seçimi */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Dönem
                </label>
                <select
                  value={period}
                  onChange={(e) => setPeriod(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="2024-12">2024 - Aralık</option>
                  <option value="2024-11">2024 - Kasım</option>
                  <option value="2024-10">2024 - Ekim</option>
                  <option value="2024-09">2024 - Eylül</option>
                  <option value="2024-08">2024 - Ağustos</option>
                  <option value="2024-07">2024 - Temmuz</option>
                </select>
              </div>

              {/* Dosya Seçimi */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  e-Defter Dosyası (XML)
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input
                    type="file"
                    accept=".xml,.XML"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600 mb-2">
                      {selectedFile ? selectedFile.name : 'XML dosyasını seçin veya sürükleyin'}
                    </p>
                    <p className="text-sm text-gray-500">
                      Maksimum dosya boyutu: 10MB
                    </p>
                  </label>
                </div>
              </div>

              {/* Örnek Dosya İndirme */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-blue-900">Örnek e-Defter Dosyası</h3>
                    <p className="text-sm text-blue-700">Test için örnek XML dosyası indirebilirsiniz</p>
                  </div>
                  <button
                    onClick={downloadSample}
                    className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    <Download className="h-4 w-4" />
                    <span>İndir</span>
                  </button>
                </div>
              </div>

              {error && (
                <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
                  <AlertCircle className="h-5 w-5" />
                  <span className="text-sm">{error}</span>
                </div>
              )}

              {/* Buttons */}
              <div className="flex items-center justify-between">
                <button
                  onClick={loadHistory}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Geçmiş Yüklemeler
                </button>
                
                <div className="flex space-x-4">
                  <button
                    onClick={onClose}
                    className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    İptal
                  </button>
                  <button
                    onClick={handleUpload}
                    disabled={!selectedFile || isUploading}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium ${
                      selectedFile && !isUploading
                        ? 'bg-blue-600 text-white hover:bg-blue-700'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    {isUploading ? (
                      <>
                        <Clock className="h-4 w-4 animate-spin" />
                        <span>Yükleniyor...</span>
                      </>
                    ) : (
                      <>
                        <Upload className="h-4 w-4" />
                        <span>Yükle</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          ) : (
            /* Upload Success */
            <div className="text-center space-y-6">
              <div className="flex items-center justify-center">
                <CheckCircle className="h-16 w-16 text-green-500" />
              </div>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  e-Defter Başarıyla Yüklendi!
                </h3>
                <p className="text-gray-600">
                  Dosya işlendi ve finansal veriler güncellendi.
                </p>
              </div>

              {/* Financial Summary */}
              <div className="bg-gray-50 rounded-lg p-6">
                <h4 className="font-medium text-gray-900 mb-4">Finansal Özet</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Toplam Varlık:</span>
                    <span className="font-medium">{formatCurrency(uploadResult.financial_summary.total_assets)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Toplam Borç:</span>
                    <span className="font-medium">{formatCurrency(uploadResult.financial_summary.total_liabilities)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Özkaynak:</span>
                    <span className="font-medium">{formatCurrency(uploadResult.financial_summary.equity)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Net Satışlar:</span>
                    <span className="font-medium">{formatCurrency(uploadResult.financial_summary.net_sales)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Cari Oran:</span>
                    <span className="font-medium">{uploadResult.financial_summary.current_ratio.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Borç/Özkaynak:</span>
                    <span className="font-medium">{uploadResult.financial_summary.debt_to_equity.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              <button
                onClick={onClose}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Tamam
              </button>
            </div>
          )}

          {/* History Modal */}
          {showHistory && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-60">
              <div className="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[80vh] overflow-y-auto">
                <div className="flex items-center justify-between p-6 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">e-Defter Geçmişi</h3>
                  <button
                    onClick={() => setShowHistory(false)}
                    className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                  >
                    ×
                  </button>
                </div>
                
                <div className="p-6">
                  {history.length === 0 ? (
                    <div className="text-center py-8">
                      <FileText className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                      <p className="text-gray-500">Henüz e-Defter yüklemesi yapılmamış</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {history.map((record) => (
                        <div key={record.id} className="border border-gray-200 rounded-lg p-4">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-3">
                              <FileText className="h-5 w-5 text-blue-600" />
                              <div>
                                <p className="font-medium text-gray-900">{record.file_name}</p>
                                <p className="text-sm text-gray-500">
                                  {record.period} • {formatFileSize(record.file_size)}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              {record.validation_status === 'valid' ? (
                                <CheckCircle className="h-5 w-5 text-green-500" />
                              ) : (
                                <AlertCircle className="h-5 w-5 text-red-500" />
                              )}
                              <span className={`text-sm font-medium ${
                                record.validation_status === 'valid' ? 'text-green-600' : 'text-red-600'
                              }`}>
                                {record.validation_status === 'valid' ? 'Geçerli' : 'Hatalı'}
                              </span>
                            </div>
                          </div>
                          
                          {record.validation_status === 'valid' && (
                            <div className="grid grid-cols-3 gap-4 text-sm mt-3 pt-3 border-t border-gray-100">
                              <div>
                                <span className="text-gray-600">Toplam Varlık:</span>
                                <p className="font-medium">{formatCurrency(record.financial_summary.total_assets)}</p>
                              </div>
                              <div>
                                <span className="text-gray-600">Net Satışlar:</span>
                                <p className="font-medium">{formatCurrency(record.financial_summary.net_sales)}</p>
                              </div>
                              <div>
                                <span className="text-gray-600">Net Kar:</span>
                                <p className="font-medium">{formatCurrency(record.financial_summary.net_profit)}</p>
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EDefterUpload;