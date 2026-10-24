# SuFix — Kampüs Arıza & Operasyon Asistanı
> **AI-Deathon – ICAAD 26** | Selçuk Üniversitesi Alaeddin Keykubat Kampüsü  
> *"Öğrenci uzman olmak zorunda değil. YZ anlatılanı teknisyenin diline çevirir, son kararı insan verir."*

---

## 🎯 Projenin Amacı ve Hipotezi
Geleneksel arıza formları kullanıcının teknik birimi önceden bilmesini bekler. Oysa öğrenci yalnızca gördüğü belirtiyi bilir.

SuFix; Telegram üzerinden gündelik dille (metin, fotoğraf, konum) gelen serbest anlatımları:
1. **Acil Durum Ön-Filtresi:** Duman, gaz kokusu, yangın gibi durumları sabit kuralla saniyeler içinde yakalayarak doğrudan `KRİTİK` öncelikle işaretler.
2. **YZ ile Yapılandırılmış İş Emri:** Belirtileri analiz eder, olası kök nedeni çıkarır, doğru birimi ve önceliği güven skoruyla önerir.
3. **Mükerrer Olay Birleştirme (Dedup):** Aynı odadaki/bölgedeki arızaları tek bir iş emrinde birleştirerek çağrı kirliliğini ve gereksiz personel seferberliğini engeller.
4. **İnsan Denetimi (Human-in-the-Loop):** Son kararı ve personel atamasını her zaman ilgili yönetici verir.

---

## 🚀 Prototipi Başlatma

### Yöntem 1: Sıfır Kurulum / Doğrudan Tarayıcıda Açma (Tavsiye Edilen)
Hiçbir paket yüklemenize (`pip install`, `npm`) gerek yoktur.
* `index.html` dosyasına çift tıklayarak doğrudan Chrome veya Edge tarayıcınızda açabilirsiniz.
* Ya da yerel sunucu ile:
```bash
python -m http.server 8000
```
Tarayıcıdan `http://localhost:8000` adresine gidin.

### Yöntem 2: FastAPI Backend ile Başlatma (Opsiyonel)
Gerekli paketleri kurup API uçlarını ayağa kaldırabilirsiniz:
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
* **Panel:** `http://localhost:8000`
* **Swagger API Dokümantasyonu:** `http://localhost:8000/docs`

---

## 🎬 6 Adımlı Sunum & Ekran Görüntüsü Senaryosu (`TODO.md` Bölüm 14)

Panelin altındaki **Senaryo Kontrol Çubuğu** veya klavyenin **Sağ / Sol Ok Tuşları** ile senaryo adımları arasında kolayca geçiş yapabilir, sunum slaytlarınız için yüksek çözünürlüklü ekran görüntüleri alabilirsiniz:

1. **Adım 1: Eksik Bilgi Bildirimi:** Öğrenci 1 sadece *"labda net yok"* yazar. Sistem konumun eksik olduğunu fark eder ve örnekli netleştirme sorusu sorar.
2. **Adım 2: YZ Analizi & Uzmanlık Boşluğu:** Öğrenci *"Mühendislik B blok 204"* yazar. YZ motoru arızayı teşhis eder:
   * **Öğrenci Tahmini:** "Elektrik" (Yanılgı!)
   * **YZ Çıkarımı:** Bilgi İşlem Daire Bşk. (Güven: %82), Neden: Switch/Port Arızası.
3. **Adım 3: Yönetici Onayı & Atama:** Yönetici kartı inceler, öneriyi onaylar ve saha personeline (Ahmet Yılmaz) iş emri olarak atar. Personel *"Üstlendim"* butonuna basar.
4. **Adım 4: Mükerrer Olay Birleştirme:** Öğrenci 2 aynı arızayı farklı cümlelerle yazar (*"bilgisayarlar internete bağlanmıyo"*). Sistem bunu açık olan #A102 nolu olayla eşleştirir; bildirim sayısı `2x` olur ve öğrenciye *"Ekibimiz şu anda bu sorun üzerinde çalışıyor"* yanıtı gider.
5. **Adım 5: Saha Çözümü (Done):** Personel işi bitirip *"Done"* butonuna basar. Her iki öğrenciye de otomatik *"Arıza giderildi"* bildirimi gider.
6. **Adım 6: Jüri Metrikleri & Kanıt:** Öğrenci yanılgı oranı (%66) ile YZ isabeti (%94.2) arasındaki fark gösterilerek sistemin yarattığı katma değer kanıtlanır.

---

## 📂 Dosya Yapısı
```
SuFix/
├── index.html              # Modern, koyu temalı tek parça Dashboard & Telegram Simülatörü
├── requirements.txt        # FastAPI & Pydantic bağımlılıkları
├── TODO.md                 # Detaylı proje şartnamesi ve mimari doküman
├── README.md               # Proje tanıtımı ve çalıştırma kılavuzu
└── app/
    ├── main.py             # FastAPI REST servisi ve index.html sunucusu
    ├── models.py           # Pydantic veri modelleri ve JSON şemaları (Bölüm 8)
    ├── ai_service.py       # Çok modlu analiz ve aynı olay tespit (dedup) servis katmanı
    └── emergency_rules.py  # Can güvenliği anahtar kelime kural motoru
```

