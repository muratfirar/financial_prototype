# Docker ile Render.com Deployment

## 🐳 Docker Avantajları
- Rust bağımlılık sorunları çözülür
- Tutarlı environment
- Daha hızlı build
- Production-ready

## 🚀 Deployment Adımları

### 1. Local Test (Opsiyonel)
```bash
cd backend
docker-compose up -d
# Test: http://localhost:8000/docs
```

### 2. GitHub Push
```bash
git add .
git commit -m "Add Docker support for Render deployment"
git push origin main
```

### 3. Render.com'da Manuel Kurulum

#### A. Database (İlk)
1. New + → PostgreSQL
2. Name: `financial-risk-db`
3. Plan: Free

#### B. Backend (Docker ile)
1. New + → Web Service
2. GitHub repo seçin
3. **Environment: Docker**
4. Root Directory: `backend`
5. Dockerfile Path: `./Dockerfile`

**Environment Variables:**
```
DATABASE_URL: (Database'den otomatik gelecek)
SECRET_KEY: (Generate butonuna tıklayın)
DEBUG: False
PORT: 10000
```

#### C. Frontend
1. New + → Static Site
2. Build Command: `npm ci && npm run build`
3. Publish Directory: `dist`

**Environment Variables:**
```
VITE_API_URL: https://financial-risk-api.onrender.com
```

## ✅ Test URLs
- Backend: `https://financial-risk-api.onrender.com/health`
- Frontend: `https://financial-risk-frontend.onrender.com`
- API Docs: `https://financial-risk-api.onrender.com/docs`

## 🔑 Test Kullanıcıları
```
admin@finansal.com / admin123
analyst@finansal.com / analyst123
```

Docker ile tüm dependency sorunları çözülecek! 🎉