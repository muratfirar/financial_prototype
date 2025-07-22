# 🚀 Local Development Setup Rehberi

## 📋 Gereksinimler

- **Python 3.8+** (Backend için)
- **Node.js 16+** (Frontend için)
- **Git** (Kod yönetimi için)

## 🛠️ Kurulum Adımları

### 1. Projeyi Klonlayın
```bash
git clone <your-repo-url>
cd financial_prototype
```

### 2. Backend Kurulumu (FastAPI + SQLite)

#### Windows:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements-local.txt
python app/main.py
```

#### macOS/Linux:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-local.txt
python app/main.py
```

**Backend çalışıyor mu kontrol edin:**
- 🌐 API: http://localhost:8000
- 📚 Docs: http://localhost:8000/docs
- ❤️ Health: http://localhost:8000/health

### 3. Frontend Kurulumu (React + Vite)

**Yeni terminal açın:**
```bash
# Ana dizinde
npm install
npm run dev
```

**Frontend çalışıyor mu kontrol edin:**
- 🌐 App: http://localhost:5173

## 🔑 Test Kullanıcıları

```
Email: admin@finansal.com
Şifre: admin123
Rol: Admin

Email: analyst@finansal.com  
Şifre: analyst123
Rol: Risk Analisti

Email: manager@finansal.com
Şifre: manager123
Rol: Yönetici
```

## 📊 Özellikler

### ✅ Çalışan Özellikler:
- ✅ Kullanıcı girişi (Mock authentication)
- ✅ Dashboard istatistikleri
- ✅ Firma listesi görüntüleme
- ✅ Firma detayları
- ✅ Yeni firma ekleme
- ✅ Firma arama ve filtreleme
- ✅ Risk dağılımı grafikleri
- ✅ SQLite veritabanı (otomatik oluşturulur)
- ✅ Örnek veriler (otomatik yüklenir)

### 🚧 Geliştirme Aşamasında:
- 🚧 Risk analizi modülü
- 🚧 Uyarı sistemi
- 🚧 Raporlama
- 🚧 Kullanıcı yönetimi

## 🗃️ Veritabanı

- **Tip:** SQLite (dosya tabanlı)
- **Konum:** `backend/financial_risk.db`
- **Otomatik:** İlk çalıştırmada oluşturulur
- **Örnek Veri:** 5 firma otomatik eklenir

## 🔧 Geliştirme İpuçları

### Backend Değişiklikleri:
- Dosyayı kaydedin → Otomatik restart (uvicorn --reload)
- API değişikliklerini http://localhost:8000/docs'ta test edin

### Frontend Değişiklikleri:
- Dosyayı kaydedin → Otomatik refresh (Vite HMR)
- Browser console'da hataları kontrol edin

### Database Sıfırlama:
```bash
# Backend dizininde
rm financial_risk.db
python app/main.py  # Yeniden oluşturulur
```

## 🐛 Sorun Giderme

### Backend Başlamıyor:
```bash
# Python versiyonu kontrol
python --version  # 3.8+ olmalı

# Bağımlılıkları yeniden yükle
pip install -r requirements-local.txt

# Port kullanımda mı?
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### Frontend Başlamıyor:
```bash
# Node versiyonu kontrol
node --version  # 16+ olmalı

# Cache temizle
rm -rf node_modules package-lock.json
npm install

# Port kullanımda mı?
lsof -i :5173  # macOS/Linux
netstat -ano | findstr :5173  # Windows
```

### CORS Hatası:
- Backend'in http://localhost:8000'de çalıştığından emin olun
- Frontend'in http://localhost:5173'te çalıştığından emin olun

## 🚀 Production'a Geçiş

Local'de test ettikten sonra:

1. **Render.com'a deploy** (mevcut setup)
2. **Docker ile deploy** (önerilen)
3. **VPS'e deploy** (advanced)

## 📞 Yardım

Sorun yaşarsanız:
1. Terminal'deki hata mesajlarını kontrol edin
2. Browser console'daki hataları kontrol edin
3. http://localhost:8000/docs API'yi test edin
4. Database dosyasını silin ve yeniden başlatın

**Happy Coding! 🎉**