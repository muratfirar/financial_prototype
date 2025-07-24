import PyPDF2
import re
import json
from typing import Dict, List, Any, Optional, Tuple
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

class TurkishTaxPDFExtractor:
    """
    Türk Kurumlar Vergisi Beyannamesi PDF'lerinden mali veri çıkarma sınıfı
    """
    
    def __init__(self):
        # Tablo başlıkları ve anahtar kelimeler
        self.table_patterns = {
            'ilaveler': [
                r'İLAVELER',
                r'EKLENEN\s+TUTARLAR',
                r'İLAVE\s+EDİLEN'
            ],
            'vergi_bildirimi': [
                r'VERGİ\s+BİLDİRİMİ',
                r'BEYAN\s+EDİLEN',
                r'VERGİ\s+MATRAH'
            ],
            'mahsup_vergiler': [
                r'MAHSUP\s+EDİLECEK\s+VERGİLER',
                r'MAHSUP\s+VERGİ',
                r'KESİNTİ\s+VE\s+MAHSUP'
            ],
            'aktif': [
                r'AKTİF',
                r'VARLIKLAR',
                r'DÖNEN\s+VARLIKLAR',
                r'DURAN\s+VARLIKLAR'
            ],
            'pasif': [
                r'PASİF',
                r'KAYNAKLAR',
                r'YABANCI\s+KAYNAKLAR',
                r'ÖZKAYNAKLAR'
            ],
            'gelir_tablosu': [
                r'GELİR\s+TABLOSU',
                r'KAPSAMLI\s+GELİR',
                r'NET\s+SATIŞ',
                r'BRÜT\s+SATIŞ'
            ]
        }
        
        # Firma bilgileri için regex pattern'ları
        self.company_patterns = {
            'tax_id': r'(?:VKN|Vergi\s+Kimlik\s+No|Tax\s+ID)[\s:]*(\d{10})',
            'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            'trade_registry': r'(?:Ticaret\s+Sicil\s+No|Trade\s+Registry)[\s:]*(\d+)',
            'commercial_profit': r'(?:Ticari\s+Bilanço\s+Karı|Commercial\s+Profit)[\s:]*([0-9.,]+)'
        }
        
        # Sayısal değer çıkarma için pattern
        self.number_pattern = r'([0-9.,]+(?:\.\d{2})?)'
        
    def extract_financial_data(self, pdf_content: bytes) -> Dict[str, Any]:
        """
        PDF'den mali verileri çıkar
        """
        try:
            # PDF'i oku
            pdf_text = self._extract_text_from_pdf(pdf_content)
            
            # Firma bilgilerini çıkar
            company_info = self._extract_company_info(pdf_text)
            
            # Tabloları çıkar
            tables = self._extract_tables(pdf_text)
            
            return {
                'success': True,
                'companyInfo': company_info,
                'tables': tables,
                'metadata': {
                    'extraction_date': self._get_current_timestamp(),
                    'total_tables_found': len([t for t in tables.values() if t]),
                    'text_length': len(pdf_text)
                }
            }
            
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'companyInfo': {},
                'tables': {}
            }
    
    def _extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """PDF'den metin çıkar"""
        try:
            pdf_file = BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text
            
        except Exception as e:
            raise Exception(f"PDF okuma hatası: {str(e)}")
    
    def _extract_company_info(self, text: str) -> Dict[str, Any]:
        """Firma bilgilerini çıkar"""
        company_info = {
            'taxId': '',
            'email': '',
            'tradeRegistryNo': '',
            'commercialProfit': 0
        }
        
        try:
            # VKN çıkar
            tax_match = re.search(self.company_patterns['tax_id'], text, re.IGNORECASE)
            if tax_match:
                company_info['taxId'] = tax_match.group(1)
            
            # E-posta çıkar
            email_match = re.search(self.company_patterns['email'], text, re.IGNORECASE)
            if email_match:
                company_info['email'] = email_match.group(1)
            
            # Ticaret sicil no çıkar
            trade_match = re.search(self.company_patterns['trade_registry'], text, re.IGNORECASE)
            if trade_match:
                company_info['tradeRegistryNo'] = trade_match.group(1)
            
            # Ticari bilanço karı çıkar
            profit_match = re.search(self.company_patterns['commercial_profit'], text, re.IGNORECASE)
            if profit_match:
                profit_str = profit_match.group(1).replace(',', '').replace('.', '')
                company_info['commercialProfit'] = float(profit_str) if profit_str.isdigit() else 0
                
        except Exception as e:
            logger.warning(f"Firma bilgileri çıkarma hatası: {str(e)}")
        
        return company_info
    
    def _extract_tables(self, text: str) -> Dict[str, Dict[str, float]]:
        """Tabloları çıkar"""
        tables = {
            'ilaveler': {},
            'vergiBildirimi': {},
            'mahsupVergiler': {},
            'aktif': {},
            'pasif': {},
            'gelirTablosu': {}
        }
        
        try:
            # Her tablo türü için çıkarma yap
            for table_name, patterns in self.table_patterns.items():
                table_data = self._extract_table_data(text, patterns)
                tables[table_name] = table_data
                
        except Exception as e:
            logger.error(f"Tablo çıkarma hatası: {str(e)}")
        
        return tables
    
    def _extract_table_data(self, text: str, patterns: List[str]) -> Dict[str, float]:
        """Belirli bir tablo türü için veri çıkar"""
        table_data = {}
        
        try:
            # Tablo başlığını bul
            table_start = None
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    table_start = match.end()
                    break
            
            if table_start is None:
                return table_data
            
            # Tablo sonunu bul (bir sonraki büyük başlık veya sayfa sonu)
            table_end = self._find_table_end(text, table_start)
            table_text = text[table_start:table_end]
            
            # Satırları işle
            lines = table_text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Satırda hem metin hem sayı var mı kontrol et
                if self._contains_financial_data(line):
                    key, value = self._parse_table_row(line)
                    if key and value is not None:
                        table_data[key] = value
                        
        except Exception as e:
            logger.warning(f"Tablo veri çıkarma hatası: {str(e)}")
        
        return table_data
    
    def _find_table_end(self, text: str, start_pos: int) -> int:
        """Tablo sonunu bul"""
        # Sonraki büyük başlıkları ara
        end_patterns = [
            r'\n[A-ZÜĞŞÇÖI]{3,}',  # Büyük harfli başlıklar
            r'\nSayfa\s+\d+',      # Sayfa numaraları
            r'\n\s*\n\s*[A-ZÜĞŞÇÖI]{3,}',  # Boş satır sonrası başlık
        ]
        
        min_end = len(text)
        for pattern in end_patterns:
            match = re.search(pattern, text[start_pos:], re.IGNORECASE)
            if match:
                end_pos = start_pos + match.start()
                min_end = min(min_end, end_pos)
        
        # Maksimum 2000 karakter al (çok uzun tabloları önlemek için)
        return min(min_end, start_pos + 2000)
    
    def _contains_financial_data(self, line: str) -> bool:
        """Satırda finansal veri var mı kontrol et"""
        # En az bir sayı ve bir metin olmalı
        has_number = bool(re.search(r'\d+', line))
        has_text = bool(re.search(r'[a-zA-ZüğşçöıÜĞŞÇÖI]{3,}', line))
        
        # Çok kısa satırları atla
        if len(line.strip()) < 5:
            return False
            
        return has_number and has_text
    
    def _parse_table_row(self, line: str) -> Tuple[Optional[str], Optional[float]]:
        """Tablo satırını anahtar-değer çiftine çevir"""
        try:
            # Sayıları bul
            numbers = re.findall(r'([0-9.,]+)', line)
            if not numbers:
                return None, None
            
            # En büyük sayıyı al (genellikle ana tutar)
            max_number = 0
            for num_str in numbers:
                try:
                    # Türk sayı formatını temizle
                    clean_num = num_str.replace(',', '').replace('.', '')
                    if clean_num.isdigit():
                        num_value = float(clean_num)
                        if num_value > max_number:
                            max_number = num_value
                except:
                    continue
            
            if max_number == 0:
                return None, None
            
            # Anahtar metni çıkar (sayıları çıkararak)
            key_text = re.sub(r'[0-9.,\s]+', ' ', line).strip()
            key_text = re.sub(r'\s+', ' ', key_text)  # Çoklu boşlukları tek yap
            
            # Çok kısa veya çok uzun anahtarları atla
            if len(key_text) < 3 or len(key_text) > 100:
                return None, None
            
            return key_text, max_number
            
        except Exception as e:
            logger.warning(f"Satır işleme hatası: {str(e)}")
            return None, None
    
    def _get_current_timestamp(self) -> str:
        """Şu anki zaman damgası"""
        from datetime import datetime
        return datetime.now().isoformat()

# Test için örnek kullanım
def create_sample_extracted_data() -> Dict[str, Any]:
    """Test için örnek çıkarılmış veri"""
    return {
        'success': True,
        'companyInfo': {
            'taxId': '1234567890',
            'email': 'info@ornek-firma.com',
            'tradeRegistryNo': '123456',
            'commercialProfit': 2500000
        },
        'tables': {
            'ilaveler': {
                'Amortisman İlavesi': 150000,
                'Karşılık İlavesi': 75000,
                'Diğer İlaveler': 25000,
                'Toplam İlaveler': 250000
            },
            'vergiBildirimi': {
                'Ticari Kar': 2500000,
                'Vergi Matrahı': 2750000,
                'Kurumlar Vergisi': 550000,
                'Geçici Vergi': 400000
            },
            'mahsupVergiler': {
                'Stopaj Vergisi': 125000,
                'Geçici Vergi': 400000,
                'Yurtdışı Vergi': 15000,
                'Toplam Mahsup': 540000
            },
            'aktif': {
                'Dönen Varlıklar': 5000000,
                'Nakit ve Nakit Benzerleri': 1200000,
                'Ticari Alacaklar': 2300000,
                'Stoklar': 1500000,
                'Duran Varlıklar': 8000000,
                'Maddi Duran Varlıklar': 6500000,
                'Maddi Olmayan Duran Varlıklar': 1500000,
                'Toplam Aktif': 13000000
            },
            'pasif': {
                'Kısa Vadeli Yükümlülükler': 3500000,
                'Ticari Borçlar': 2000000,
                'Diğer Borçlar': 1500000,
                'Uzun Vadeli Yükümlülükler': 2000000,
                'Finansal Borçlar': 1800000,
                'Özkaynaklar': 7500000,
                'Ödenmiş Sermaye': 5000000,
                'Geçmiş Yıl Karları': 2000000,
                'Net Dönem Karı': 500000,
                'Toplam Pasif': 13000000
            },
            'gelirTablosu': {
                'Brüt Satışlar': 15000000,
                'Satış İndirimları': 500000,
                'Net Satışlar': 14500000,
                'Satışların Maliyeti': 10000000,
                'Brüt Kar': 4500000,
                'Faaliyet Giderleri': 3200000,
                'Faaliyet Karı': 1300000,
                'Finansman Giderleri': 200000,
                'Vergi Öncesi Kar': 1100000,
                'Vergi Gideri': 220000,
                'Net Dönem Karı': 880000
            }
        },
        'metadata': {
            'extraction_date': '2025-01-22T10:30:00',
            'total_tables_found': 6,
            'text_length': 15420
        }
    }