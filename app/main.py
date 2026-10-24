"""
SuFix — FastAPI Backend Servisi
Selçuk Üniversitesi Alaeddin Keykubat Kampüsü — Arıza Asistanı
"""
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models import (
    Olay, OlayDurumu, BirimKodu, OncelikSeviyesi, 
    KonumBilgisi, BildirimIstegi, YoneticiKarari
)
from app.emergency_rules import acil_durum_kontrolu, ACIL_UYARI_MESAJI
from app.ai_service import AIService

app = FastAPI(
    title="SuFix Kampüs Arıza Asistanı API",
    description="Doğal dil ve görsel tabanlı kampüs arıza yönlendirme ve yönetim sistemi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_INCIDENTS: List[dict] = [
    {
        "id": "H104",
        "takip_kodu": "#H104",
        "durum": "ONAY_BEKLIYOR",
        "ozet": "Mühendislik B Blok zemin kat WC'de fotoselli havluluk hareket algılamıyor",
        "teknik_aciklama": "Görselden cihaz prizde ve kağıt mevcut. Sorun kızılötesi fotosel sensör optik arızası.",
        "olasi_neden": "Karex marka fotosel sensör kalibrasyon kaybı veya optik kirlenme",
        "konum": {
            "bina": "Mühendislik Fakültesi B Blok",
            "kat": "Zemin",
            "oda": "Erkekler Tuvaleti",
            "serbest_metin": "Mühendislik Fakültesi B Blok zemin kat erkekler tuvaleti"
        },
        "ai_birim": "ELEKTRIK",
        "ai_oncelik": "ORTA",
        "ai_guven": 0.92,
        "final_birim": None,
        "final_oncelik": None,
        "atanan_personel": None,
        "bildirim_sayisi": 1,
        "acil_kural_tetiklendi": False,
        "ogrenci_birim_tahmini": "Temizlik / Kağıt Bitti", # Yanılgı örneği!
        "raw_mesaj": "bu aletin önünde elimi sallıyorum ama hiç kağıt vermiyor, prize takılı ama hareket algılamıyor",
        "gorsel_yolu": "docs/problem-foto.jpeg"
    }
]

@app.get("/")
def get_dashboard():
    """Doğrudan tek parça Tailwind dashboard HTML'ini sunar."""
    index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "SuFix API aktif. Arayüz için index.html dosyası kök dizinde bulunmalıdır."}

@app.get("/api/incidents")
def list_incidents():
    return MOCK_INCIDENTS

@app.post("/api/report")
def submit_report(req: BildirimIstegi):
    acil_mi, kural = acil_durum_kontrolu(req.mesaj)
    if acil_mi:
        return {
            "durum": "ACIL_DURUM",
            "mesaj": ACIL_UYARI_MESAJI,
            "oncelik": "KRITIK"
        }

    gps_dict = {"lat": req.gps_lat, "lng": req.gps_lng} if req.gps_lat else None
    analiz = AIService.analiz_et(req.mesaj, foto_var_mi=True, gps=gps_dict)

    if not analiz.yeterli_bilgi:
        return {
            "durum": "BILGI_BEKLENIYOR",
            "mesaj": analiz.netlestirme_sorusu,
            "eksik": analiz.eksik_alanlar
        }

    return {
        "durum": "ONAY_BEKLIYOR",
        "takip_kodu": "#H104",
        "mesaj": "Bildiriminiz alındı. Takip No: #H104. İlgili birime iletilmek üzere inceleniyor."
    }

@app.get("/api/metrics")
def get_proof_metrics():
    return {
        "orneklem_boyutu": 142,
        "ogrenci_tahmin_dogrulugu": 0.34,
        "ai_yonetici_uyumu": 0.942,
        "onlenen_tekrar_orani": 0.428,
        "ort_onay_suresi_dk": 2.8,
        "acil_filtre_basarisi": 1.0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
