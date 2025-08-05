# 📊 TEV KPI & Aksiyon Takip Modülü

Bu proje, Türk Eğitim Vakfı’nın KPI ve aksiyon yönetimini kolaylaştırmak için geliştirilmiş bir Streamlit uygulamasıdır.

## 🚀 Özellikler

- Giriş ekranı ve kullanıcı doğrulama (MongoDB destekli)
- KPI ve aksiyon ekleme, güncelleme, loglama
- Strateji bazlı KPI takibi
- Timeline görünümü
- Raporlama ve görselleştirme
- Şifre maskeli kullanıcı yönetimi
- Excel dışa aktarma ve dosya yükleme özellikleri

## 🏗️ Klasör Yapısı
aksiyonModulu/
│
├── aksiyon_kpi_modulu/
│ ├── config.py
│ ├── database.py
│ ├── auth.py
│ ├── utils.py
│ ├── ui_main.py
│ └── pages/
│ ├── 1_📝_Aksiyon_Ekle.py
│ ├── 2_📊_Aksiyon_Guncelle.py
│ ├── 3_📈_Raporlama.py
│ ├── 4_📅_Takvim.py
│ ├── 5_🕓_Log.py
│ ├── 6_👤_Kullanici_Yonetimi.py
│ └── 7_📋_Acik_Isler.py
│
├── requirements.txt
├── README.md

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
streamlit run aksiyon_kpi_modulu/ui_main.py

Gereken Dosyalar
Aşağıdaki dosyalar proje dizininde bulunmalıdır:

TEV_2024_KPI.xlsx

Aksiyonlar.xlsx

kullanicilar.xlsx

MongoDB'in localhost:27017'de çalışıyor olması gerekir.

📬 İletişim
Bu modül, TEV Dijital Dönüşüm kapsamında geliştirilmiştir.
"""

Dosyaları kaydet
with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
f.write(requirements.strip())

with open(os.path.join(base_dir, "README.md"), "w") as f:
f.write(readme.strip())
