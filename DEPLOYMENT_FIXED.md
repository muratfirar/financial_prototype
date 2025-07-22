# Render.com Deployment Rehberi - Düzeltilmiş

## 🚀 Adım Adım Deployment

### 1. GitHub Repository Hazırlığı
```bash
# Değişiklikleri push edin
git add .
git commit -m "Fix: Remove Rust dependencies for Render deployment"
git push origin main
```

### 2. Render.com'da Manuel Kurulum

#### A. PostgreSQL Database (İlk)
1. Render Dashboard → "New +" → "PostgreSQL"
2. Ayarlar:
   - **Name:** `financial-risk-db`
   - **Database:** `financial_risk_db`
   - **User:** `financial_user`
   - **Region:** Frankfurt
   - **Plan:** Free
3. "Create Database" → Database URL'i kopyalayın

#### B. Backend API (İkinci)
1. "New +" → "Web Service"
2. GitHub repo seçin
3. Ayarlar:
   - **Name:** `financial-risk-api`
   - **Environment:** Python 3
   - **Root Directory:** `backend`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. **Environment Variables (Manuel Ekleyin):**
   ```
   DATABASE_URL: postgresql://financial_user:PASSWORD@HOST:PORT/financial_risk_db
   SECRET_KEY: your-generated-secret-key-here
   DEBUG: False
   ```
sadasdsadasd 
#### C. Backend Deploy Sonrası
Backend çalıştıktan sonra Shell'den:
```bash
alembic upgrade head
python create_sample_data.py
```

#### D. Frontend (Son)
1. "New +" → "Static Site"
2. Ayarlar:
   - **Name:** `financial-risk-frontend`
   - **Build Command:** `npm ci && npm run build`
   - **Publish Directory:** `dist`

3. **Environment Variables:**
   ```
   VITE_API_URL: https://financial-prototype-docker.onrender.com
   ```

## 🔧 Sorun Giderme

- Backend: `https://financial-prototype-docker.onrender.com/health`
- API Docs: `https://financial-prototype-docker.onrender.com/docs`
1. Database servisinizin "Info" sekmesinden External Database URL'i kopyalayın
2. Backend servisinizin Environment Variables'a ekleyin

### Test URLs
- Backend: `https://financial-risk-api.onrender.com/health`
- Frontend: `https://financial-risk-frontend.onrender.com`
- API Docs: `https://financial-risk-api.onrender.com/docs`

### Test Kullanıcıları
```
admin@finansal.com / admin123
analyst@finansal.com / analyst123
```

## 🚨 Önemli Notlar
- Free plan'da ilk istek 30-60 saniye sürebilir (cold start)
- Database URL'i manuel olarak kopyalamanız gerekebilir
- Her GitHub push otomatik deploy tetikler