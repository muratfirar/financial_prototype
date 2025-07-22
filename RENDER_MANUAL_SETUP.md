# Render.com Manuel Kurulum Rehberi

## 🚨 Hostname Sorunu Çözümü

Render.com'da Docker container'lar external database hostname'ine erişemiyor. Bu yüzden migration'ları manuel yapacağız.

## 🚀 Deployment Adımları

### 1. GitHub'a Push
```bash
git add .
git commit -m "Fix: Remove migrations from startup, add manual setup"
git push origin main
```

### 2. Render.com'da Kurulum

#### A. Database (İlk)
- PostgreSQL → Name: `financial-risk-db`
- Plan: Free

#### B. Backend (İkinci)
- Web Service → Environment: Docker
- Root Directory: `backend`

**Environment Variables:**
```
DATABASE_URL: postgresql://financial_user:VPqOnEoHcIOOk0GmFto3IzniH6O1eaNU@dpg-d1vuqcali9vc73ft4a3g-a/financial_risk_db
SECRET_KEY: (Generate)
DEBUG: False
PORT: 10000
```

### 3. Manuel Setup (ÖNEMLİ!)

Backend deploy edildikten sonra:

1. **Render Dashboard** → Backend servisiniz → **"Shell"** sekmesi
2. Şu komutları çalıştırın:

```bash
# Migration'ları çalıştır
alembic upgrade head

# Sample data oluştur
python manual_setup.py
```

### 4. Frontend
- Static Site → Normal kurulum
- Environment: `VITE_API_URL: https://your-backend-url.onrender.com`

## ✅ Test

- Backend: `https://your-backend.onrender.com/health`
- API Docs: `https://your-backend.onrender.com/docs`

## 🔑 Test Kullanıcıları

```
admin@finansal.com / admin123
analyst@finansal.com / analyst123
```

Bu yaklaşımla hostname sorunu tamamen aşılacak! 🎉