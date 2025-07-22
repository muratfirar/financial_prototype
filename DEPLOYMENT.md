# Render.com Deployment Rehberi

## 🚀 Adım Adım Deployment

### 1. GitHub Repository Oluşturma
```bash
# Projeyi GitHub'a push edin
git init
git add .
git commit -m "Initial commit: Financial Risk Management Platform"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/financial-risk-platform.git
git push -u origin main
```

### 2. Render.com'da Hesap Oluşturma
1. https://render.com adresine gidin
2. GitHub hesabınızla giriş yapın
3. Repository'nizi bağlayın

### 3. Database Kurulumu
1. Render Dashboard'da "New +" butonuna tıklayın
2. "PostgreSQL" seçin
3. Ayarlar:
   - Name: `financial-risk-db`
   - Database: `financial_risk_db`
   - User: `financial_user`
   - Region: Frankfurt (Avrupa için)
   - Plan: Free

### 4. Backend API Kurulumu
1. "New +" → "Web Service" seçin
2. GitHub repository'nizi seçin
3. Ayarlar:
   - Name: `financial-risk-api`
   - Environment: Python 3
   - Build Command: `cd backend && pip install -r requirements.txt && alembic upgrade head`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free

4. Environment Variables:
   - `DATABASE_URL`: PostgreSQL connection string (otomatik)
   - `SECRET_KEY`: Generate edilecek
   - `CORS_ORIGINS`: `["https://FRONTEND_URL.onrender.com"]`

### 5. Frontend Kurulumu
1. "New +" → "Static Site" seçin
2. Ayarlar:
   - Name: `financial-risk-frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

3. Environment Variables:
   - `VITE_API_URL`: `https://financial-risk-api.onrender.com`

### 6. Domain Ayarları
- Backend: `https://financial-risk-api.onrender.com`
- Frontend: `https://financial-risk-frontend.onrender.com`
- Database: Internal connection

## 🔧 Deployment Sonrası

### Test Kullanıcıları
```
admin@finansal.com / admin123
analyst@finansal.com / analyst123
manager@finansal.com / manager123
```

### API Endpoints
- Swagger UI: `https://financial-risk-api.onrender.com/docs`
- Health Check: `https://financial-risk-api.onrender.com/health`

## 🚨 Önemli Notlar

1. **Free Plan Limitleri:**
   - Database: 1GB storage
   - Backend: 512MB RAM, sleep after 15 min inactivity
   - Frontend: 100GB bandwidth

2. **Cold Start:**
   - Free plan'da servisler 15 dakika sonra uyur
   - İlk istek 30-60 saniye sürebilir

3. **Environment Variables:**
   - Production'da güçlü SECRET_KEY kullanın
   - CORS_ORIGINS'i doğru domain'le güncelleyin

## 🔄 Continuous Deployment

GitHub'a her push'da otomatik deploy olur:
```bash
git add .
git commit -m "Feature: New functionality"
git push origin main
```

## 📊 Monitoring

Render Dashboard'dan:
- Logs görüntüleme
- Metrics takibi
- Error monitoring
- Performance analytics