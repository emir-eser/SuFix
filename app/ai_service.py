"""
SuFix — Yapay Zeka Servis Katmanı (PROJECT.md Bölüm 7)

Bu servis gerçek Gemini/Claude çok modlu (multimodal) API çağrısı yapabilecek arayüze sahiptir;
Ideathon demosu için deterministik ve hatasız mock çıktılar üretir.
"""
from typing import Optional, List, Dict, Any
from app.models import AIAnalizCiktisi, AIDedupCiktisi, BirimKodu, OncelikSeviyesi, KonumBilgisi

class AIService:
    @staticmethod
    def analiz_et(mesaj: str, foto_var_mi: bool = False, foto_yolu: Optional[str] = None, gps: Optional[Dict[str, float]] = None) -> AIAnalizCiktisi:
        """
        Çağrı 1: Gündelik dili ve görseli analiz eder, bilgi yeterliliğini denetler ve teknik iş emrine dönüştürür.
        """
        metin_alt = mesaj.lower()

        # Konum kontrolü
        konum_anahtarlari = ["blok", "kat", "wc", "tuvalet", "oda", "lab", "kütüphane", "derslik", "otopark", "fakülte", "zemin"]
        konum_belirtilmis = any(k in metin_alt for k in konum_anahtarlari) or (gps is not None)

        if not konum_belirtilmis:
            return AIAnalizCiktisi(
                yeterli_bilgi=False,
                eksik_alanlar=["konum"],
                netlestirme_sorusu="Fotoğrafı ve arıza bildirimini aldım! Fotoselli havlulukta hareket sensörü arızası tespit edildi. Ekiplerimizin müdahale edebilmesi için bu tuvaletin fakülte, blok ve kat bilgisini yazar mısınız? (Örn: Mühendislik B Blok zemin kat erkekler wc)",
                guven=0.3
            )

        # Senaryo: Fotoselli Havluluk Sensör Arızası (docs/problem-foto.jpeg)
        if foto_var_mi or any(w in metin_alt for w in ["havlu", "alet", "sensör", "elimi", "kağıt", "fotosel", "tuvalet", "wc"]):
            return AIAnalizCiktisi(
                yeterli_bilgi=True,
                ozet="Mühendislik B Blok zemin kat WC'de fotoselli havluluk hareket algılamıyor.",
                teknik_aciklama="Görselde cihaz prizden enerji alıyor, rulo kağıt mevcut. Alt oval sensör penceresindeki kızılötesi (PIR) fotosel merceği optik kirlenmesi veya kart temassızlığı mevcut.",
                olasi_neden="Fotosel optik sensör arızası veya kalibrasyon kaybı (Karex marka).",
                konum=KonumBilgisi(
                    bina="Mühendislik Fakültesi B Blok",
                    kat="Zemin",
                    oda="Erkekler Tuvaleti",
                    serbest_metin=mesaj,
                    gps=gps
                ),
                birim=BirimKodu.ELEKTRIK,
                birim_gerekce="Fotoselli elektronik cihaz ve sensör arızası (Yapı İşleri Elektrik/Donanım).",
                oncelik=OncelikSeviyesi.ORTA,
                oncelik_gerekce="Hijyen aksaması yaratıyor ancak acil can güvenliği tehlikesi yok.",
                guven=0.92,
                gorsel_bulgular="Cihaz duvara monteli, prize takılı, haznede kağıt mevcut, sensör tetiklenmiyor."
            )

        # Varsayılan
        return AIAnalizCiktisi(
            yeterli_bilgi=True,
            ozet=f"Genel Kampüs Bildirimi: {mesaj[:50]}...",
            teknik_aciklama="Ayrıntılı teknik teşhis için yerinde inceleme gerekli.",
            olasi_neden="Belirsiz teknik aksaklık.",
            konum=KonumBilgisi(serbest_metin=mesaj, gps=gps),
            birim=BirimKodu.DIGER,
            birim_gerekce="Kategori netleştirilemedi.",
            oncelik=OncelikSeviyesi.ORTA,
            oncelik_gerekce="Varsayılan öncelik.",
            guven=0.60
        )

    @staticmethod
    def ayni_olay_kontrolu(yeni_bildirim: AIAnalizCiktisi, acik_olaylar: List[Dict[str, Any]]) -> AIDedupCiktisi:
        """
        Çağrı 2: Yeni bildirimin açık olan başka bir olayla aynı kök nedene dayanıp dayanmadığını doğrular.
        """
        for olay in acik_olaylar:
            bina_ayni = (olay.get("bina") == (yeni_bildirim.konum.bina if yeni_bildirim.konum else None))
            birim_ayni = (olay.get("birim") == yeni_bildirim.birim)
            
            if bina_ayni and birim_ayni:
                return AIDedupCiktisi(
                    eslesen_olay_id=olay.get("id"),
                    ayni_sorun_mu=True,
                    gerekce="Aynı tuvalette aynı fotoselli havluluk için farklı kullanıcı anlatımıyla bildirilen mükerrer sorun."
                )

        return AIDedupCiktisi(
            eslesen_olay_id=None,
            ayni_sorun_mu=False,
            gerekce="Konum veya sorun tipi eşleşen açık bir olay bulunamadı; bağımsız yeni kayıt oluşturulmalı."
        )
