# 🎯 Aksiyon ve KPI Yönetim Modülü

Bu proje, kurum içi performans hedeflerini (KPI) ve bu hedeflere yönelik aksiyonları yönetmek amacıyla geliştirilmiş kullanıcı dostu bir Python / Streamlit uygulamasıdır.

## 🚀 Özellikler

- ✅ KPI tanımlama ve güncelleme
- ✅ Aksiyon planı oluşturma
- ✅ Dosya (kanıt belgesi) yükleme ve takibi
- ✅ Kullanıcı ve birim bazlı yetkilendirme
- ✅ Raporlama, filtreleme ve grafikle analiz
- ✅ Zaman çizelgesi (timeline) görselleştirme
- ✅ Admin paneli ile kullanıcı yönetimi

---

## 🖥️ Kullanılan Teknolojiler

- [Python 3.9+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Openpyxl & XlsxWriter](https://openpyxl.readthedocs.io/)

---

## 📁 Proje Yapısı

aksiyonModulu/
│
├── app.py # Ana uygulama dosyası
├── config.py # Dosya yolları
├── utils.py # Yardımcı fonksiyonlar
├── requirements.txt
├── README.md
│
├── pages/ # Sayfa modülleri
│ ├── aksiyon_ekle.py
│ ├── aksiyon_guncelle.py
│ ├── aksiyon_raporlama.py
│ ├── kullanici_yonetimi.py
│ └── timeline.py
│
└── data/ # Veri dosyaları
├── TEV_2024_KPI.xlsx
├── kullanicilar.xlsx
├── log_kpi_guncelleme.xlsx
├── Aksiyonlar.xlsx
└── kanitlar/ # Yüklenen belgeler klasörü


---

## ⚙️ Kurulum

1. Bu repoyu klonla:

```bash
git clone https://github.com/burhanozen29/aksiyonModulu.git
cd aksiyonModulu

2. Gerekli kütüphaneleri yükle:
pip install -r requirements.txt

3. Uygulamayı çalıştır:
streamlit run app.py

Notlar
Uygulama sadece .xlsx dosyaları ile çalışır, veritabanı kullanılmaz.

Geliştirme ortamı: Spyder / VSCode / Jupyter + Anaconda

Proje geliştirme aşamasındadır, geri bildirimlerinize açığız.

📬 İletişim
Burhan Özen
📧 burhan.ozen@outlook.com
🔗 GitHub: @burhanozen29
