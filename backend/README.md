# Financial Risk Management Platform - Backend

Bu proje, finansal risk yönetimi için geliştirilmiş kapsamlı bir backend API'sidir. FastAPI, SQLAlchemy ve PostgreSQL kullanılarak geliştirilmiştir.

## 🚀 Özellikler

### Temel Modüller
- **Kullanıcı Yönetimi**: Rol tabanlı yetkilendirme sistemi
- **Firma Yönetimi**: Firma bilgileri ve finansal veriler
- **Risk Analizi**: Gelişmiş risk skorlama algoritmaları
- **Erken Uyarı Sistemi**: Otomatik risk tespit ve uyarılar
- **Dashboard**: Kapsamlı istatistikler ve raporlama
- **Finansal Metrikler**: Detaylı finansal analiz

### Kullanıcı Rolleri
- **Admin**: Sistem yönetimi ve tüm yetkiler
- **Manager**: Yönetici seviyesi erişim
- **Risk Analyst**: Risk analizi ve firma yönetimi
- **Data Observer**: Sadece okuma yetkisi
- **Dealer**: Kendi firmalarına özel erişim

### Risk Analizi Özellikleri
- Kredi risk skorlama (0-1000)
- PD (Probability of Default) hesaplama
- Sektör bazlı risk ayarlamaları
- Finansal sağlık değerlendirmesi
- Otomatik kredi limit önerisi
- Stres test analizleri

## 🛠️ Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### 1. Projeyi İndirin
```bash
git clone <repository-url>
cd backend
```

### 2. Virtual Environment Oluşturun
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Veritabanı Kurulumu
```bash
# PostgreSQL'i yükleyin (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# PostgreSQL servisini başlatın
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Veritabanı ve kullanıcı oluşturun
sudo -u postgres psql

CREATE DATABASE financial_risk_db;
CREATE USER financial_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE financial_risk_db TO financial_user;
\q
```

### 5. Environment Variables Ayarlayın
```bash
# .env dosyası oluşturun
cp .env.example .env

# .env dosyasını düzenleyin
nano .env
```

**.env dosyası örneği:**
```env
DATABASE_URL=postgresql://financial_user:your_password@localhost:5432/financial_risk_db
SECRET_KEY=your-super-secret-key-here-change-in-production
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### 6. Veritabanı Migration'larını Çalıştırın
```bash
# Alembic migration'larını başlatın
alembic upgrade head
```

### 7. Örnek Veri Oluşturun (Opsiyonel)
```bash
python scripts/create_sample_data.py
```

### 8. Sunucuyu Başlatın
```bash
# Development sunucusu
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Veya direkt olarak
python app/main.py
```

API şu adreste çalışacak: `http://localhost:8000`

## 📚 API Dokümantasyonu

### Swagger UI
API dokümantasyonuna şu adresten erişebilirsiniz:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Ana Endpoint'ler

#### Authentication
- `POST /api/v1/auth/login` - Kullanıcı girişi
- `POST /api/v1/auth/register` - Yeni kullanıcı kaydı

#### Companies
- `GET /api/v1/companies/` - Firma listesi
- `POST /api/v1/companies/` - Yeni firma oluştur
- `GET /api/v1/companies/{id}` - Firma detayları
- `PUT /api/v1/companies/{id}` - Firma güncelle
- `POST /api/v1/companies/{id}/recalculate-risk` - Risk yeniden hesapla

#### Risk Analysis
- `GET /api/v1/risk-analysis/` - Risk analizleri listesi
- `POST /api/v1/risk-analysis/` - Yeni risk analizi
- `POST /api/v1/risk-analysis/{company_id}/quick-analysis` - Hızlı analiz

#### Alerts
- `GET /api/v1/alerts/` - Uyarılar listesi
- `PUT /api/v1/alerts/{id}/read` - Uyarıyı okundu işaretle
- `PUT /api/v1/alerts/{id}/resolve` - Uyarıyı çözümle

#### Dashboard
- `GET /api/v1/dashboard/stats` - Dashboard istatistikleri
- `GET /api/v1/dashboard/recent-activities` - Son aktiviteler
- `GET /api/v1/dashboard/risk-trends` - Risk trendleri

## 🧪 Test Etme

### Unit Testleri Çalıştırın
```bash
pytest tests/ -v
```

### Test Coverage
```bash
pytest --cov=app tests/
```

### API Testleri
```bash
# Postman collection'ı import edin veya curl kullanın
curl -X GET "http://localhost:8000/health"
```

## 🔧 Geliştirme

### Yeni Migration Oluşturma
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Kod Formatı
```bash
# Black formatter
black app/

# Import sorting
isort app/
```

### Linting
```bash
flake8 app/
```

## 📊 Risk Skorlama Algoritması

### Kredi Risk Skoru (0-1000)
- **Finansal Sağlık** (35%): Karlılık, likidite, kaldıraç oranları
- **Ödeme Geçmişi** (25%): Geçmiş ödeme performansı
- **Sektör Riski** (15%): Sektörel risk çarpanları
- **Makroekonomik** (10%): Genel ekonomik koşullar
- **Likidite** (15%): Nakit akışı ve likidite oranları

### PD (Probability of Default) Hesaplama
Lojistik regresyon modeli kullanılarak:
- Borç/Özkaynak oranı
- Cari oran
- Aktif karlılığı (ROA)
- Sektörel ayarlamalar

### Risk Seviyeleri
- **Düşük Risk**: 750-1000 puan
- **Orta Risk**: 600-749 puan  
- **Yüksek Risk**: 400-599 puan
- **Kritik Risk**: 0-399 puan

## 🚀 Production Deployment

### Docker ile Deployment
```bash
# Dockerfile oluşturun
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables (Production)
```env
DATABASE_URL=postgresql://user:password@db-host:5432/financial_risk_db
SECRET_KEY=very-secure-secret-key-for-production
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
```

### Nginx Konfigürasyonu
```nginx
server {
    listen 80;
    server_name your-api-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📝 Örnek Kullanım

### 1. Kullanıcı Girişi
```python
import requests

# Login
response = requests.post("http://localhost:8000/api/v1/auth/login", 
    data={
        "username": "analyst@finansal.com",
        "password": "analyst123"
    }
)
token = response.json()["access_token"]

# Headers for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
```

### 2. Firma Oluşturma
```python
company_data = {
    "name": "Yeni Firma A.Ş.",
    "tax_id": "1111111111",
    "sector": "Teknoloji",
    "revenue": 15000000,
    "assets": 10000000,
    "liabilities": 4000000,
    "credit_limit": 3000000
}

response = requests.post(
    "http://localhost:8000/api/v1/companies/",
    json=company_data,
    headers=headers
)
```

### 3. Risk Analizi
```python
# Hızlı risk analizi
response = requests.post(
    f"http://localhost:8000/api/v1/risk-analysis/{company_id}/quick-analysis",
    params={"analysis_type": "credit"},
    headers=headers
)
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 Destek

Sorularınız için:
- Email: support@finansal.com
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)

## 🔄 Changelog

### v1.0.0 (2025-01-21)
- İlk sürüm yayınlandı
- Temel risk analizi modülleri
- Kullanıcı yönetimi sistemi
- Dashboard ve raporlama
- Otomatik uyarı sistemi