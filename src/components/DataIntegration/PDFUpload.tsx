import React, { useState } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle, Download, Eye, Trash2 } from 'lucide-react';

interface ExtractedData {
  companyInfo: {
    taxId: string;
    email: string;
    tradeRegistryNo: string;
    commercialProfit: number;
  };
  tables: {
    ilaveler: Record<string, number>;
    vergiBildirimi: Record<string, number>;
    mahsupVergiler: Record<string, number>;
    aktif: Record<string, number>;
    pasif: Record<string, number>;
    gelirTablosu: Record<string, number>;
  };
}

const PDFUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [extractedData, setExtractedData] = useState<ExtractedData | null>(null);
  const [error, setError] = useState('');
  const [uploadHistory, setUploadHistory] = useState<any[]>([]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError('');
      setExtractedData(null);
    } else {
      setError('Lütfen geçerli bir PDF dosyası seçin');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Lütfen bir PDF dosyası seçin');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('pdf', selectedFile);

      const response = await fetch('/api/v1/pdf/extract-financial-data', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('PDF işleme başarısız');
      }

      const result = await response.json();
      setExtractedData(result);
      
      // Add to history
      setUploadHistory(prev => [{
        id: Date.now(),
        fileName: selectedFile.name,
        uploadDate: new Date().toISOString(),
        status: 'success',
        data: result
      }, ...prev]);

    } catch (err) {
      setError('PDF dosyası işlenirken hata oluştu');
    } finally {
      setIsProcessing(false);
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

  const downloadExtractedData = () => {
    if (!extractedData) return;

    const dataStr = JSON.stringify(extractedData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `extracted_data_${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-3 mb-6">
          <FileText className="h-6 w-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">PDF Mali Veri Çıkarma</h2>
        </div>

        <div className="space-y-6">
          {/* File Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Kurumlar Vergisi Beyannamesi (PDF)
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="hidden"
                id="pdf-upload"
              />
              <label htmlFor="pdf-upload" className="cursor-pointer">
                <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-2">
                  {selectedFile ? selectedFile.name : 'PDF dosyasını seçin veya sürükleyin'}
                </p>
                <p className="text-sm text-gray-500">
                  Maksimum dosya boyutu: 50MB
                </p>
              </label>
            </div>
          </div>

          {/* Processing Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-medium text-blue-900 mb-2">Çıkarılacak Veriler:</h3>
            <div className="grid grid-cols-2 gap-4 text-sm text-blue-700">
              <div>
                <p>• Vergi Kimlik Numarası (VKN)</p>
                <p>• E-Posta Adresi</p>
                <p>• Ticaret Sicil No</p>
                <p>• Ticari Bilanço Karı</p>
              </div>
              <div>
                <p>• İlaveler Tablosu</p>
                <p>• Vergi Bildirimi Tablosu</p>
                <p>• Mahsup Edilecek Vergiler</p>
                <p>• Aktif/Pasif ve Gelir Tablosu</p>
              </div>
            </div>
          </div>

          {error && (
            <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
              <AlertCircle className="h-5 w-5" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          {/* Upload Button */}
          <div className="flex justify-end">
            <button
              onClick={handleUpload}
              disabled={!selectedFile || isProcessing}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium ${
                selectedFile && !isProcessing
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {isProcessing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>İşleniyor...</span>
                </>
              ) : (
                <>
                  <Upload className="h-4 w-4" />
                  <span>PDF'i İşle</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Processing Status */}
      {isProcessing && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">PDF İşleniyor</h3>
            <p className="text-gray-600 mb-4">
              Dosya analiz ediliyor ve mali veriler çıkarılıyor...
            </p>
            <div className="space-y-2 text-sm text-gray-500">
              <p>✓ PDF dosyası okunuyor</p>
              <p>✓ Tablo yapıları tespit ediliyor</p>
              <p>✓ Mali veriler çıkarılıyor</p>
              <p>⏳ Veriler doğrulanıyor</p>
            </div>
          </div>
        </div>
      )}

      {/* Extracted Data Display */}
      {extractedData && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <CheckCircle className="h-6 w-6 text-green-600" />
              <h3 className="text-lg font-semibold text-gray-900">Çıkarılan Mali Veriler</h3>
            </div>
            <button
              onClick={downloadExtractedData}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              <Download className="h-4 w-4" />
              <span>JSON İndir</span>
            </button>
          </div>

          {/* Company Info */}
          <div className="mb-6">
            <h4 className="font-medium text-gray-900 mb-3">Firma Bilgileri</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
              <div>
                <p className="text-sm text-gray-600">VKN</p>
                <p className="font-medium">{extractedData.companyInfo.taxId}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">E-Posta</p>
                <p className="font-medium">{extractedData.companyInfo.email}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Ticaret Sicil No</p>
                <p className="font-medium">{extractedData.companyInfo.tradeRegistryNo}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Ticari Bilanço Karı</p>
                <p className="font-medium">{formatCurrency(extractedData.companyInfo.commercialProfit)}</p>
              </div>
            </div>
          </div>

          {/* Tables Data */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* İlaveler */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-3">İlaveler</h4>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {Object.entries(extractedData.tables.ilaveler).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-gray-600">{key}:</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Vergi Bildirimi */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-3">Vergi Bildirimi</h4>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {Object.entries(extractedData.tables.vergiBildirimi).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-gray-600">{key}:</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Aktif */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-3">Aktif</h4>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {Object.entries(extractedData.tables.aktif).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-gray-600">{key}:</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Pasif */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-3">Pasif</h4>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {Object.entries(extractedData.tables.pasif).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-gray-600">{key}:</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Gelir Tablosu */}
            <div className="border border-gray-200 rounded-lg p-4 lg:col-span-2">
              <h4 className="font-medium text-gray-900 mb-3">Gelir Tablosu</h4>
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(extractedData.tables.gelirTablosu).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-gray-600">{key}:</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Upload History */}
      {uploadHistory.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">İşleme Geçmişi</h3>
          <div className="space-y-3">
            {uploadHistory.map((item) => (
              <div key={item.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-blue-600" />
                  <div>
                    <p className="font-medium text-gray-900">{item.fileName}</p>
                    <p className="text-sm text-gray-500">
                      {new Date(item.uploadDate).toLocaleString('tr-TR')}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    item.status === 'success' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {item.status === 'success' ? 'Başarılı' : 'Hatalı'}
                  </span>
                  <button
                    onClick={() => setExtractedData(item.data)}
                    className="p-1 text-gray-600 hover:text-gray-900 rounded"
                    title="Görüntüle"
                  >
                    <Eye className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => setUploadHistory(prev => prev.filter(h => h.id !== item.id))}
                    className="p-1 text-red-600 hover:text-red-900 rounded"
                    title="Sil"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PDFUpload;