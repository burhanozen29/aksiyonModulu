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
│   └── Açık_İşler.py
│
├── requirements.txt
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

