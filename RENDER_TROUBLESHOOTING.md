# Render.com Troubleshooting Guide

## 🔧 Database Connection Issues

### Problem: `DATABASE_URL` is empty
**Solution:**
1. Database servisinizin tamamen deploy olmasını bekleyin
2. Backend servisini database'den sonra oluşturun
3. Environment Variables'da DATABASE_URL'i manuel kontrol edin

### Manual DATABASE_URL Setup:
1. Database servisinizin "Info" sekmesine gidin
2. "External Database URL"i kopyalayın
3. Backend servisinizin Environment Variables'ına ekleyin

## 🚀 Correct Deployment Order

### 1. Database First
```
New + → PostgreSQL
Name: financial-risk-db
Plan: Free
```

### 2. Wait for Database (Important!)
Database status "Available" olana kadar bekleyin (2-5 dakika)

### 3. Backend Second
```
New + → Web Service
Environment: Docker
Root Directory: backend
```

**Environment Variables:**
```
DATABASE_URL: (Database'den kopyalayın)
SECRET_KEY: (Generate)
DEBUG: False
PORT: 10000
```

### 4. Frontend Last
```
New + → Static Site
Build Command: npm ci && npm run build
Publish Directory: dist
```

## 🔍 Debug Commands

Backend Shell'den test edin:
```bash
# Environment variables kontrol
env | grep DATABASE

# Database bağlantısı test
python -c "from app.core.config import settings; print(settings.DATABASE_URL)"

# Manuel migration
alembic upgrade head

# Sample data
python create_sample_data.py
```

## 📊 Expected URLs
- Database: Internal only
- Backend: https://financial-risk-api.onrender.com
- Frontend: https://financial-risk-frontend.onrender.com
- API Docs: https://financial-risk-api.onrender.com/docs

## ⚠️ Common Issues

1. **Cold Start**: İlk istek 30-60 saniye sürebilir
2. **Database URL**: Manuel kopyalamanız gerekebilir  
3. **Build Order**: Database → Backend → Frontend sırası önemli
4. **Environment Variables**: Büyük/küçük harf duyarlı

Bu adımları takip ederek deployment başarılı olacak! 🎉