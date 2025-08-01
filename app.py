# app.py

import streamlit as st
from utils import kullanici_dogrula
from pages import (
    aksiyon_ekle,
    aksiyon_guncelle,
    aksiyon_raporlama,
    guncelleme_gecmisi,
    kullanici_yonetimi,
    timeline,
)

# === Oturum kontrolü ===
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False

# === Giriş ekranı ===
if not st.session_state.giris_yapildi:
    def giris_yap(otomatik=False):
        sonuc = kullanici_dogrula(st.session_state.kullanici_input, st.session_state.sifre)
        if sonuc:
            st.session_state.giris_yapildi = True
            st.session_state.kullanici = st.session_state.kullanici_input
            st.session_state.birimler = sonuc["birimler"]
            st.session_state.rol = sonuc["rol"]
            if not otomatik:
                st.rerun()
        else:
            st.session_state.hata_mesaji = "❌ Kullanıcı adı veya şifre hatalı."

    st.title("🔐 KPI Takip Sistemi - Giriş")
    st.text_input("Kullanıcı Adı", key="kullanici_input")
    st.text_input("Şifre", type="password", key="sifre", on_change=giris_yap, kwargs={"otomatik": True})

    if st.button("Giriş Yap"):
        giris_yap(otomatik=False)

    if "hata_mesaji" in st.session_state:
        st.error(st.session_state.hata_mesaji)

    st.stop()

# === Menü ve sayfa yönlendirme ===
st.sidebar.title("📁 Menü")
menu_items = ["Aksiyon Ekle", "Aksiyon Güncelle", "Raporlama", "Takvim"]
if st.session_state.rol == "admin":
    menu_items.append(["Güncelleme Geçmişi","Kullanıcı Yönetimi"])

secim = st.sidebar.radio("İşlem seçin:", menu_items)

if secim == "Aksiyon Ekle":
    aksiyon_ekle.run()
elif secim == "Aksiyon Güncelle":
    aksiyon_guncelle.run()
elif secim == "Raporlama":
    aksiyon_raporlama.run()
elif secim == "Takvim":
    timeline.run()
elif secim == "Güncelleme Geçmişi":
    guncelleme_gecmisi.run()
elif secim == "Kullanıcı Yönetimi":
    kullanici_yonetimi.run()
