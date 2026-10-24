"""
SuFix — Yapay Zeka Servis Katmanı (TODO.md Bölüm 7)

Bu servis gerçek Gemini/Claude API çağrısı yapabilecek arayüze sahiptir;
Ideathon demosu için deterministik ve hatasız mock çıktılar üretir.
"""
from typing import Optional, List, Dict, Any
from app.models import AIAnalizCiktisi, AIDedupCiktisi, BirimKodu, OncelikSeviyesi, KonumBilgisi

class AIService:
    @staticmethod
    def analiz_et(mesaj: str, foto_var_mi: bool = False, gps: Optional[Dict[str, float]] = None) -> AIAnalizCiktisi:
        """
        Çağrı 1: Gündelik dili analiz eder, bilgi yeterliliğini denetler ve teknik iş emrine dönüştürür.
        """
        metin_alt = mesaj.lower()

        # Senaryo 1: Eksik konum kontrolü ("labda net yok", "burası damlıyo" vb.)
        konum_anahtarlari = ["blok", "kat", "oda", "lab", "kütüphane", "derslik", "otopark", "fakülte", "204", "104"]
        konum_belirtilmis = any(k in metin_alt for k in konum_anahtarlari) or (gps is not None)

        if not konum_belirtilmis:
            return AIAnalizCiktisi(
                yeterli_bilgi=False,
                eksik_alanlar=["konum"],
                netlestirme_sorusu="Sorunun nerede olduğunu anlayamadım. Kampüsümüzde hızla müdahale edebilmemiz için bina, kat ve mümkünse oda numarasını yazar mısın? (Örn: Mühendislik B blok 2. kat 204 nolu lab)",
                guven=0.3
            )

        # Senaryo 2: Ağ / Bilgi İşlem ("internet", "net yok", "wifi", "kablolu")
        if any(w in metin_alt for w in ["net", "internet", "bağlanmıyo", "kablolu", "wifi"]):
            return AIAnalizCiktisi(
                yeterli_bilgi=True,
                ozet="Mühendislik B Blok 204 nolu labda kablolu internet çalışmıyor, Wi-Fi faal.",
                teknik_aciklama="Sorun kablolu ağ ile ve tek odayla sınırlı görünüyor. Kablosuz ağ çalıştığı için fakülte omurgasında kesinti olası değil.",
                olasi_neden="Odadaki kenar ağ anahtarı (edge switch) veya Ethernet priz port arızası.",
                konum=KonumBilgisi(
                    bina="Mühendislik Fakültesi B Blok",
                    kat="2",
                    oda="204",
                    serbest_metin=mesaj,
                    gps=gps
                ),
                birim=BirimKodu.BILGI_ISLEM,
                birim_gerekce="Kablolu yerel ağ (LAN) erişim arızası.",
                oncelik=OncelikSeviyesi.YUKSEK,
                oncelik_gerekce="Ders ve laboratuvar uygulamalarını doğrudan engelliyor.",
                guven=0.82
            )

        # Senaryo 3: Elektrik ("priz", "ışık", "elektrik", "lamba")
        if any(w in metin_alt for w in ["priz", "ışık", "lamba", "elektrik", "şalter"]):
            return AIAnalizCiktisi(
                yeterli_bilgi=True,
                ozet="B blok 204 nolu labda priz gruplarına enerji gelmiyor.",
                teknik_aciklama="İlgili odadaki tali panoya ait sigorta grubu devreden çıkmış veya hat kopukluğu mevcut.",
                olasi_neden="Aşırı yük sebebiyle sigorta atması.",
                konum=KonumBilgisi(
                    bina="Mühendislik Fakültesi B Blok",
                    kat="2",
                    oda="204",
                    serbest_metin=mesaj,
                    gps=gps
                ),
                birim=BirimKodu.ELEKTRIK,
                birim_gerekce="Priz ve aydınlatma şebekesi arızası.",
                oncelik=OncelikSeviyesi.ORTA,
                oncelik_gerekce="Cihaz kullanımını aksatıyor fakat hayati tehlike yok.",
                guven=0.91
            )

        # Senaryo 4: Tesisat / Su sızıntısı
        if any(w in metin_alt for w in ["damlıyo", "su", "sızıntı", "musluk", "asansör"]):
            return AIAnalizCiktisi(
                yeterli_bilgi=True,
                ozet="Tavanda su damlaması ve kabarma tespit edildi.",
                teknik_aciklama="Üst kat temiz/pis su hattında kaçak şüphesi.",
                olasi_neden="Üst kat tesisat borusunda contadan sızma.",
                konum=KonumBilgisi(
                    bina="Merkezi Derslikler",
                    kat="1",
                    oda="102",
                    serbest_metin=mesaj,
                    gps=gps
                ),
                birim=BirimKodu.TESISAT,
                birim_gerekce="Sıhhi tesisat ve bina yapı arızası.",
                oncelik=OncelikSeviyesi.YUKSEK,
                oncelik_gerekce="Binanın fiziki yapısına ve alt kata zarar verme riski.",
                guven=0.88
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
            # Aynı bina ve aynı oda/kat kontrolü
            bina_ayni = (olay.get("bina") == (yeni_bildirim.konum.bina if yeni_bildirim.konum else None))
            birim_ayni = (olay.get("birim") == yeni_bildirim.birim)
            
            if bina_ayni and birim_ayni:
                return AIDedupCiktisi(
                    eslesen_olay_id=olay.get("id"),
                    ayni_sorun_mu=True,
                    gerekce="Aynı odada aynı ağ/sistem altyapısına dair farklı kullanıcı anlatımıyla bildirilen mükerrer sorun."
                )

        return AIDedupCiktisi(
            eslesen_olay_id=None,
            ayni_sorun_mu=False,
            gerekce="Konum veya sorun tipi eşleşen açık bir olay bulunamadı; bağımsız yeni kayıt oluşturulmalı."
        )

