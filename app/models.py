"""
SuFix — Veri Modelleri ve Şemaları (TODO.md Bölüm 8)
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Durum Tanımları (Bölüm 5.3)
class OlayDurumu(str, Enum):
    BILGI_BEKLENIYOR = "BILGI_BEKLENIYOR"
    ONAY_BEKLIYOR = "ONAY_BEKLIYOR"
    ATANDI = "ATANDI"
    ISLEMDE = "ISLEMDE"
    COZULDU = "COZULDU"
    REDDEDILDI = "REDDEDILDI"
    ZAMAN_ASIMI = "ZAMAN_ASIMI"

# Birim Tanımları (Bölüm 6.2)
class BirimKodu(str, Enum):
    BILGI_ISLEM = "BILGI_ISLEM"
    ELEKTRIK = "ELEKTRIK"
    TESISAT = "TESISAT"
    TEMIZLIK = "TEMIZLIK"
    GUVENLIK = "GUVENLIK"
    ULASIM = "ULASIM"
    DIGER = "DIGER"

# Öncelik Tanımları (Bölüm 6.3)
class OncelikSeviyesi(str, Enum):
    KRITIK = "KRITIK"
    YUKSEK = "YUKSEK"
    ORTA = "ORTA"
    DUSUK = "DUSUK"

# Konum Şeması
class KonumBilgisi(BaseModel):
    bina: Optional[str] = None
    kat: Optional[str] = None
    oda: Optional[str] = None
    serbest_metin: str
    gps: Optional[Dict[str, float]] = None

# YZ Çağrı 1 Çıktı Şeması (Bölüm 7.2)
class AIAnalizCiktisi(BaseModel):
    yeterli_bilgi: bool
    eksik_alanlar: List[str] = Field(default_factory=list)
    netlestirme_sorusu: Optional[str] = None
    ozet: Optional[str] = None
    teknik_aciklama: Optional[str] = None
    olasi_neden: Optional[str] = None
    konum: Optional[KonumBilgisi] = None
    birim: Optional[BirimKodu] = None
    birim_gerekce: Optional[str] = None
    oncelik: Optional[OncelikSeviyesi] = None
    oncelik_gerekce: Optional[str] = None
    guven: float = 0.0
    gorsel_bulgular: Optional[str] = None

# YZ Çağrı 2 Çıktı Şeması (Bölüm 7.3)
class AIDedupCiktisi(BaseModel):
    eslesen_olay_id: Optional[str] = None
    ayni_sorun_mu: bool
    gerekce: str

# Öğrenci Bildirim İsteği
class BildirimIstegi(BaseModel):
    mesaj: str
    ogrenci_chat_id: str = "mock_chat_123"
    ogrenci_birim_tahmini: Optional[str] = None
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None

# Yönetici Karar İsteği
class YoneticiKarari(BaseModel):
    aksiyon: str # "ONAYLA", "DEGISTIR", "REDDET"
    final_birim: Optional[BirimKodu] = None
    final_oncelik: Optional[OncelikSeviyesi] = None
    atanan_personel_id: Optional[str] = None
    red_nedeni: Optional[str] = None

# Olay Görüntüleme Modeli
class Olay(BaseModel):
    id: str
    takip_kodu: str
    durum: OlayDurumu
    ozet: str
    teknik_aciklama: str
    olasi_neden: str
    konum: KonumBilgisi
    ai_birim: BirimKodu
    ai_oncelik: OncelikSeviyesi
    ai_guven: float
    final_birim: Optional[BirimKodu] = None
    final_oncelik: Optional[OncelikSeviyesi] = None
    atanan_personel: Optional[str] = None
    bildirim_sayisi: int = 1
    acil_kural_tetiklendi: bool = False
    olusturulma: datetime = Field(default_factory=datetime.now)

