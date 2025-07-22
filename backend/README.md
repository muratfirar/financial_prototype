# Financial Risk Management Platform - Backend

FastAPI tabanlı finansal risk yönetimi platformu backend'i.

## 🚀 Hızlı Başlangıç

### Docker ile Çalıştırma (Önerilen)

```bash
# Projeyi klonlayın
git clone <your-repo>
cd backend

# Docker ile çalıştırın
docker-compose up -d

# Veritabanı migration'larını çalıştırın
docker-compose exec api alembic upgrade head

# Örnek veri oluşturun
docker-compose exec api python create_sample_data.py
```

### Manuel Kurulum

```bash
# Virtual environment oluşturun
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# PostgreSQL kurulumu
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb financial_risk_db
sudo -u postgres createuser financial_user
sudo -u postgres psql -c "ALTER USER financial_user WITH PASSWORD 'financial_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE financial_risk_db TO financial_user;"

# Environment variables
cp .env.example .env
# .env dosyasını düzenleyin

# Migration'lar
alembic upgrade head

# Örnek veri
python create_sample_data.py

# Sunucuyu başlatın
uvicorn app.main:app --reload
```

## 📚 API Dokümantasyonu

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔑 Test Kullanıcıları

```
Admin: admin@finansal.com / admin123
Manager: manager@finansal.com / manager123
Risk Analyst: analyst@finansal.com / analyst123
Data Observer: observer@finansal.com / observer123
Dealer: dealer@finansal.com / dealer123
```

## 🏗️ Mimari

- **FastAPI**: Modern, hızlı web framework
- **SQLAlchemy**: ORM ve veritabanı yönetimi
- **PostgreSQL**: Ana veritabanı
- **JWT**: Authentication ve authorization
- **Alembic**: Veritabanı migration'ları
- **Pydantic**: Veri validasyonu

## 📁 Proje Yapısı

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Core configuration
│   ├── models/          # SQLAlchemy models
│   └── schemas/         # Pydantic schemas
├── alembic/             # Database migrations
├── docker-compose.yml   # Docker configuration
└── requirements.txt     # Python dependencies
```

## 🔧 Geliştirme

```bash
# Yeni migration oluşturma
alembic revision --autogenerate -m "Description"
alembic upgrade head

# Test çalıştırma
pytest

# Kod formatı
black app/
isort app/
```