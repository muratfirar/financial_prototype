from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import require_analyst_access
from app.models.user import User
from app.services.pdf_extractor import TurkishTaxPDFExtractor, create_sample_extracted_data
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/extract-financial-data")
async def extract_financial_data_from_pdf(
    pdf: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
) -> Dict[str, Any]:
    """
    PDF'den mali verileri çıkar
    """
    
    # Dosya türü kontrolü
    if pdf.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sadece PDF dosyaları kabul edilir"
        )
    
    # Dosya boyutu kontrolü (50MB)
    if pdf.size and pdf.size > 50 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dosya boyutu 50MB'dan büyük olamaz"
        )
    
    try:
        # PDF içeriğini oku
        pdf_content = await pdf.read()
        
        # PDF extractor'ı başlat
        extractor = TurkishTaxPDFExtractor()
        
        # Verileri çıkar
        extracted_data = extractor.extract_financial_data(pdf_content)
        
        if not extracted_data['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"PDF işleme hatası: {extracted_data.get('error', 'Bilinmeyen hata')}"
            )
        
        # Log the extraction
        logger.info(f"PDF extraction successful for user {current_user.id}, file: {pdf.filename}")
        
        return extracted_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF işleme sırasında beklenmeyen bir hata oluştu"
        )

@router.get("/sample-data")
def get_sample_extracted_data(
    current_user: User = Depends(require_analyst_access)
) -> Dict[str, Any]:
    """
    Test için örnek çıkarılmış veri döndür
    """
    return create_sample_extracted_data()

@router.post("/validate-extracted-data")
def validate_extracted_data(
    data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
) -> Dict[str, Any]:
    """
    Çıkarılan verileri doğrula ve tutarlılık kontrolleri yap
    """
    
    validation_results = {
        'isValid': True,
        'warnings': [],
        'errors': [],
        'suggestions': []
    }
    
    try:
        company_info = data.get('companyInfo', {})
        tables = data.get('tables', {})
        
        # VKN kontrolü
        tax_id = company_info.get('taxId', '')
        if not tax_id or len(tax_id) != 10 or not tax_id.isdigit():
            validation_results['errors'].append('Geçerli bir VKN bulunamadı')
            validation_results['isValid'] = False
        
        # Bilanço dengesi kontrolü
        aktif = tables.get('aktif', {})
        pasif = tables.get('pasif', {})
        
        total_aktif = aktif.get('Toplam Aktif', 0)
        total_pasif = pasif.get('Toplam Pasif', 0)
        
        if total_aktif > 0 and total_pasif > 0:
            balance_diff = abs(total_aktif - total_pasif)
            balance_ratio = balance_diff / max(total_aktif, total_pasif)
            
            if balance_ratio > 0.01:  # %1'den fazla fark
                validation_results['warnings'].append(
                    f'Bilanço dengesi uyumsuz: Aktif {total_aktif:,.0f} TL, Pasif {total_pasif:,.0f} TL'
                )
        
        # Gelir tablosu tutarlılık kontrolü
        gelir = tables.get('gelirTablosu', {})
        net_satis = gelir.get('Net Satışlar', 0)
        brut_satis = gelir.get('Brüt Satışlar', 0)
        
        if brut_satis > 0 and net_satis > brut_satis:
            validation_results['errors'].append('Net satışlar brüt satışlardan büyük olamaz')
            validation_results['isValid'] = False
        
        # Kar tutarlılık kontrolü
        faaliyet_kari = gelir.get('Faaliyet Karı', 0)
        net_kar = gelir.get('Net Dönem Karı', 0)
        ticari_kar = company_info.get('commercialProfit', 0)
        
        if faaliyet_kari > 0 and net_kar > faaliyet_kari:
            validation_results['warnings'].append('Net kar faaliyet karından büyük görünüyor')
        
        # Öneriler
        if total_aktif > 0:
            validation_results['suggestions'].append(
                f'Toplam aktif: {total_aktif:,.0f} TL - Firma büyüklüğü orta ölçekli görünüyor'
            )
        
        if net_satis > 0 and net_kar > 0:
            kar_marji = (net_kar / net_satis) * 100
            validation_results['suggestions'].append(
                f'Net kar marjı: %{kar_marji:.2f} - {"İyi" if kar_marji > 5 else "Düşük"} karlılık'
            )
        
    except Exception as e:
        validation_results['errors'].append(f'Doğrulama hatası: {str(e)}')
        validation_results['isValid'] = False
    
    return validation_results

@router.post("/create-company-from-pdf")
def create_company_from_pdf_data(
    data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_access)
) -> Dict[str, Any]:
    """
    PDF'den çıkarılan verilerle yeni firma oluştur
    """
    try:
        from app.models.company import Company, RiskLevel, FinancialHealth, CompanyStatus
        from app.schemas.company import CompanyCreate
        
        company_info = data.get('companyInfo', {})
        tables = data.get('tables', {})
        
        # Firma bilgilerini hazırla
        aktif = tables.get('aktif', {})
        pasif = tables.get('pasif', {})
        gelir = tables.get('gelirTablosu', {})
        
        company_data = CompanyCreate(
            name=f"Firma - {company_info.get('taxId', 'Bilinmeyen')}",
            tax_id=company_info.get('taxId', ''),
            sector="Bilinmeyen",  # PDF'den çıkarılamadı
            revenue=gelir.get('Net Satışlar', 0),
            assets=aktif.get('Toplam Aktif', 0),
            liabilities=pasif.get('Toplam Pasif', 0) - pasif.get('Özkaynaklar', 0),
            credit_limit=0  # Hesaplanacak
        )
        
        # Firmayı veritabanına kaydet
        from app.api.v1.companies import create_company
        new_company = create_company(company_data, db, current_user)
        
        return {
            'success': True,
            'company': new_company,
            'message': 'Firma PDF verilerinden başarıyla oluşturuldu'
        }
        
    except Exception as e:
        logger.error(f"Company creation from PDF error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Firma oluşturma hatası: {str(e)}"
        )