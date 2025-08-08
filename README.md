# 📊 TEV Aksiyon Takip Modülü

Bu proje, Türk Eğitim Vakfı’nın KPI ve aksiyon yönetimini kolaylaştırmak için geliştirilmiş bir Streamlit uygulamasıdır.

## 🚀 Özellikler

- Giriş ekranı ve kullanıcı doğrulama
- KPI ve aksiyon ekleme, güncelleme
- Gelişmiş loglama
- Strateji bazlı KPI takibi
- Timeline görünümü
- Raporlama ve görselleştirme
- Şifre maskeli kullanıcı yönetimi
- Excel dışa aktarma ve dosya yükleme özellikleri
- Yaklaşan aksiyonların Mail ile bildirimi
- Onay mekanizması

## Eklenecek Özellikler

- Oluşturulan aksiyonların mail ile bildirimi (Yeni aksiyon tanımlandığında sistem, ilgili kişilere (sorumlu kişi, işi yapacak kişi) otomatik e-posta gönderir. Opsiyonel olarak "onay bekliyor" statüsünde olur ve yöneticinin onayına sunulur. Onay mekanizması için:Yetkili kullanıcı için onay ekranı (yeni sayfa: “Aksiyon Onay Paneli”)Onay/Reddet butonları, açıklama alanı)
- Yönetici Dashboardu (Tüm raporlar, filtreler, aksiyonlar. KPI doluluk oranları, tamamlanma yüzdesi, en çok geciken işler, en aktif kullanıcılar gibi göstergeler)
- Etkinlik Değerlendirmesi (aksiyon tamamlandıktan sonra Gerçekten işe yaradı mı?Sürdürülebilir mi?Kontrol edildi mi? )
- Aksiyon Risk Önem Seviyesi


## 📁 Klasör Yapısı

```text
aksiyonModulu/
│
├── aksiyon_kpi_modulu/
│   ├── config.py
│   ├── database.py
│   ├── auth.py
│   ├── utils.py
│
├── pages/
│   ├── Aksiyon_Ekle.py
│   ├── Aksiyon_Güncelle.py
│   ├── Raporlama.py
│   ├── Takvim.py
│   ├── Log.py
│   ├── Kullanıcı_Yönetimi.py
│   ├── Onay_Bekleyenler.py
│   └── Açık_İşler.py
│
├── requirements.txt
├── termin_uyarisi.py
├── Anasayfa.py
├── README.md
├── run.py
```

## 💻 Kurulum

```bash
# 1. Repo'yu klonla
git clone https://github.com/burhanozen29/aksiyonModulu.git
cd aksiyonModulu

# 2. Ortamı hazırla
python -m venv venv
source venv/bin/activate   # (Linux/macOS)
venv\\Scripts\\activate    # (Windows)

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Uygulamayı başlat
streamlit run Anasayfa.py
```

# Gereken Dosyalar
Aşağıdaki dosyalar proje dizininde bulunmalıdır:

TEV_2024_KPI.xlsx
Aksiyonlar.xlsx
kullanicilar.xlsx
mail_pass.txt

MongoDB'in localhost:27017'de çalışıyor olması gerekir.

📬 İletişim
Bu modül, TEV Dijital Dönüşüm kapsamında geliştirilmiştir.
"""






