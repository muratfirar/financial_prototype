# Render.com Database URL Rehberi

## 🔍 Database URL Türleri

Render.com'da 2 farklı database URL türü var:

### 1. External Database URL (Dışarıdan Erişim)
```
postgresql://financial_user:VPqOnEoHcIOOk0GmFto3IzniH6O1eaNU@dpg-d1vuqcali9vc73ft4a3g-a/financial_risk_db
```
- ❌ Docker container'lardan erişilemiyor
- ✅ Sadece dış uygulamalardan kullanılır

### 2. Internal Database URL (Container'lardan Erişim)
```
postgresql://financial_user:VPqOnEoHcIOOk0GmFto3IzniH6O1eaNU@dpg-d1vuqcali9vc73ft4a3g-a.oregon-postgres.render.com/financial_risk_db
```
- ✅ Docker container'lardan erişilebilir
- ✅ Render servisleri arası iletişim

## 🚀 Nasıl Bulunur?

### Yöntem 1: Render Dashboard
1. Database servisinize gidin
2. "Info" sekmesine tıklayın
3. "Internal Database URL" kısmını kopyalayın

### Yöntem 2: Otomatik Conversion (Kodda)
Kodumuz external URL'i otomatik olarak internal'a çeviriyor:
- `dpg-xxx-a` → `dpg-xxx-a.oregon-postgres.render.com`

## 🔧 Environment Variable Ayarı

Backend servisinizde:

**Eğer Internal URL varsa:**
```
DATABASE_URL: postgresql://user:pass@dpg-xxx-a.oregon-postgres.render.com/db
```

**Eğer sadece External URL varsa:**
```
DATABASE_URL: postgresql://user:pass@dpg-xxx-a/db
```
(Kod otomatik olarak internal'a çevirecek)

## ✅ Test

Deploy sonrası backend loglarında şunu göreceksiniz:
```
Database URL: postgresql://...@dpg-xxx-a.oregon-postgres.render.com/...
```

Bu internal hostname ile bağlantı başarılı olacak! 🎉