# 🚀 Hızlı Başlangıç Rehberi

## 📋 Gereksinimler
- Python 3.8+ 
- Node.js 16+

## ⚡ Adım Adım Kurulum

### 1. Backend Kurulumu (Terminal 1)
```bash
# Backend klasörüne git
cd backend

# Virtual environment oluştur
python -m venv venv

# Virtual environment'ı aktif et
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements-local.txt

# Backend'i başlat
python start_local.py
```

### 2. Frontend Kurulumu (Terminal 2 - Yeni Terminal)
```bash
# Ana klasörde kal
# Node bağımlılıklarını yükle
npm install

# Frontend'i başlat
npm run dev
```

## 🔗 Erişim URL'leri
- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🔑 Test Kullanıcıları
- **admin@finansal.com** / **admin123** (Admin)
- **analyst@finansal.com** / **analyst123** (Risk Analisti)
- **manager@finansal.com** / **manager123** (Yönetici)

## 🐛 Sorun Giderme

### Backend Başlamıyor:
```bash
# Virtual environment aktif mi kontrol et
which python  # Linux/Mac
where python  # Windows

# Bağımlılıkları tekrar yükle
pip install --upgrade pip
pip install -r requirements-local.txt
```

### Frontend Backend'e Bağlanamıyor:
1. Backend'in http://localhost:8000'de çalıştığından emin ol
2. Browser'da http://localhost:8000/health adresini test et
3. CORS hatası varsa backend'i yeniden başlat

### Port Kullanımda:
```bash
# Port 8000 kullanımda mı kontrol et
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Farklı port kullan
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)"
```

## ✅ Başarılı Kurulum Kontrolü
1. Backend: http://localhost:8000/health → `{"status": "healthy"}`
2. Frontend: http://localhost:5173 → Login ekranı görünmeli
3. API Docs: http://localhost:8000/docs → Swagger UI açılmalı

## 🔄 Geliştirme Döngüsü
1. **Backend değişiklik:** Otomatik reload (uvicorn --reload)
2. **Frontend değişiklik:** Otomatik refresh (Vite HMR)
3. **Database sıfırlama:** `financial_risk.db` dosyasını sil, backend'i yeniden başlat

Happy Coding! 🎉