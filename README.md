# SuFix — Kampüs Arıza & Operasyon Asistanı
> **AI-Deathon – ICAAD 26** | Selçuk Üniversitesi Alaeddin Keykubat Kampüsü  
> *"Öğrenci uzman olmak zorunda değil. YZ anlatılanı teknisyenin diline çevirir, son kararı insan verir."*

---

## 🎯 Projenin Amacı ve Hipotezi
Geleneksel arıza formları kullanıcının teknik birimi önceden bilmesini bekler. Oysa öğrenci yalnızca gördüğü belirtiyi bilir.

SuFix; mobil uygulama üzerinden öğrencilerin gündelik dille yazdığı serbest anlatımları:
1. **SuFix Mobil & AI Asistanı:** Öğrenci karmaşık formlar doldurmaz; mobil uygulama içi sohbet ekranında gördüğü sorunu yazar. Eksik bilgi varsa asistan yönlendirir.
2. **Kargo Takip Tarzı Şeffaflık:** Öğrenci arızanın durumunu kargo teslimat süreci gibi adım adım (Bildirim Alındı → YZ Analiz Etti → Birime Atandı → Ekip Sahada → Çözüldü & Kapatıldı) canlı takip eder.
3. **YZ ile Yapılandırılmış Teşhis:** Belirtileri analiz eder, olası kök nedeni çıkarır, yetkili birimi ve önceliği güven skoruyla önerir.
4. **Mükerrer Olay Birleştirme (Dedup):** Aynı odadaki/bölgedeki arızaları tek bir iş emrinde birleştirerek çağrı kirliliğini ve gereksiz personel çıkışını %42.8 oranında engeller.
5. **İnsan Denetimi (Human-in-the-Loop):** Son kararı ve personel atamasını her zaman ilgili yönetici verir.

---

## 🚀 Prototipi Başlatma

### Yöntem 1: Sıfır Kurulum / Doğrudan Tarayıcıda Açma (Tavsiye Edilen)
Hiçbir paket yüklemenize (`pip install`, `npm`) gerek yoktur.
* `index.html` dosyasına çift tıklayarak doğrudan Chrome veya Edge tarayıcınızda açabilirsiniz.
* Ya da yerel sunucu ile:
```powershell
python -m http.server 8000
```
Tarayıcıdan `http://localhost:8000` adresine gidin.

### Yöntem 2: FastAPI Backend ile Başlatma (Opsiyonel)
Gerekli paketleri kurup API uçlarını ayağa kaldırabilirsiniz:
```powershell
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
* **Panel:** `http://localhost:8000`
* **Swagger API Dokümantasyonu:** `http://localhost:8000/docs`

---

## 🎬 6 Adımlı Sunum & Ekran Görüntüsü Senaryosu

Panelin üstündeki **Senaryo Kontrol Çubuğu** veya klavyenin **Sağ / Sol Ok Tuşları** ile senaryo adımları arasında kolayca geçiş yapabilir, sunum slaytlarınız için yüksek çözünürlüklü ekran görüntüleri alabilirsiniz:

1. **Adım 1: Eksik Bilgi Bildirimi:** Öğrenci mobil asistan ekranında sadece *"hocam labda net yok makineler açılmıyor ders yapamıyoruz"* yazar. Asistan konumun eksik olduğunu fark eder ve örnekli soru sorar.
2. **Adım 2: YZ Analizi & Kargo Takip Başlangıcı:** Öğrenci *"Mühendislik B blok 2. kat 204"* yazar. YZ motoru arızayı teşhis eder (`#A102` Takip Kodu üretilir):
   * **Öğrenci Tahmini:** "Elektrik" (Yanılgı!)
   * **YZ Çıkarımı:** Bilgi İşlem Daire Bşk. (Güven: %88), Neden: Switch/Port Arızası.
   * Öğrenci tek tıkla **"Kargo Takip"** ekranına geçip sürecin 2. adımda olduğunu görür.
3. **Adım 3: Yönetici Onayı & Atama:** Yönetici kartı inceler, öneriyi onaylar ve saha personeline (Ahmet Yılmaz) iş emri atar. Kargo takip ekranında 3. adım yeşile döner (*"Teknisyene Atandı"*).
4. **Adım 4: Mükerrer Olay Birleştirme:** 2. öğrenci aynı arızayı yazdığında sistem bunu açık olan #A102 ile eşleştirir; bildirim sayısı `2x` olur ve kargo sürecinde *"Ekip Sahada Müdahale Ediyor"* aşaması görünür.
5. **Adım 5: Saha Çözümü (Done):** Teknisyen işi bitirdiğinde kargo takip ekranında tüm aşamalar tamamlanır (*"Çözüldü & Kapatıldı"*).
6. **Adım 6: Jüri Analitiği & Kanıt:** Öğrenci yanılgı oranı (%66) ile YZ isabeti (%94.2) arasındaki fark gösterilerek sistemin yarattığı katma değer kanıtlanır.

---

## 👥 Ekip Bilgileri (AI-Deathon · ICAAD 26)
* Ali Kemal Akdeniz
* Yusufcan Özdemir
* Emir Eser
* Dagimawi Moges Wakumo
