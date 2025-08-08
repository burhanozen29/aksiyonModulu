# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:12:41 2025

@author: bozen
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from aksiyon_kpi_modulu.utils import aktif_ceyrek_bul
from aksiyon_kpi_modulu.auth import kullanici_dogrula
import pandas as pd

st.set_page_config(page_title="Giriş", page_icon="🔐", layout="wide")
# === Oturum yönetimi ===
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False
    st.set_option("client.showSidebarNavigation", False)

if not st.session_state.giris_yapildi:
    
    def giris_yap(otomatik=False):
        sonuc = kullanici_dogrula(st.session_state.kullanici_input, st.session_state.sifre)
        if sonuc:
            st.session_state.giris_yapildi = True
            st.session_state.kullanici = st.session_state.kullanici_input
            st.session_state.birimler = sonuc["birimler"]
            st.session_state.rol = sonuc["rol"]
            st.session_state.bagli_kisi = sonuc["bagli_kisi"]
            st.session_state.bagli_birim = sonuc["bagli_birim"]
            st.session_state.isim = sonuc["isim"]
            st.set_option("client.showSidebarNavigation", True)
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



# Kullanıcı bilgileri

st.set_page_config(page_title="Anasayfa", layout="wide")
kullanici = st.session_state.get("kullanici", "Bilinmiyor")
rol = st.session_state.get("rol", "Yok")
if not rol or pd.isna(rol):
    rol = "Yok"
birimler = st.session_state.get("birimler", [])
bagli_birim = st.session_state.get("bagli_birim","")
bagli_kisi = st.session_state.get("bagli_kisi","")
isim = st.session_state.get("isim","")

# Başlık ve karşılama
st.title("📊 TEV KPI & Aksiyon Takip Platformu")
st.markdown(f"""
Merhaba **{isim}** 👋  
Bu platform üzerinden birim bazlı aksiyonlarını ve KPI gelişimlerini kolayca takip edebilirsin.

---
""")

# Sol ve sağ kolon
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🧾 Bilgilerin")
    st.markdown(f"""
    **Kullanıcı Rolü:** `{rol}`  
    **Tanımlı Birim:** `{birimler[0]}`  
    **Bağlı Birim:** `{bagli_birim}`
    **Bağlı Kişi:** `{bagli_kisi}`
    """)
    st.markdown("📆 **Aktif Çeyrek:** " + f"`{aktif_ceyrek_bul()}`")

with col2:
    if rol == "Yok":
        st.subheader("🛠️ Kullanabileceğin Modüller")
        st.markdown("""
        - 📝 **Aksiyon Ekle:** Yeni bir aksiyon tanımla
        - 📊 **Aksiyon Güncelle:** Mevcut aksiyon ve KPI'ları güncelle
        - 📈 **Raporlama:** Filtrele, analiz et, Excel'e aktar
        - 📅 **Takvim Görünümü:** Zaman çizelgesi ile aksiyonları izle
        - 📋 **Açık İşler:** Üzerine tanımlı işler listesi
        - ✅ **Onay Bekleyenler:** Aksiyonların sonuçlarını değerlendirip onaylama/reddetme
        """)
    else:
        st.subheader("🛠️ Kullanabileceğin Modüller")
        st.markdown("""
        - 📝 **Aksiyon Ekle:** Yeni bir aksiyon tanımla
        - 📊 **Aksiyon Güncelle:** Mevcut aksiyon ve KPI'ları güncelle
        - 📈 **Raporlama:** Filtrele, analiz et, Excel'e aktar
        - 📅 **Takvim Görünümü:** Zaman çizelgesi ile aksiyonları izle
        - 🕓 **Geçmiş Loglar:** Güncellenen KPI geçmişini görüntüle
        - 📋 **Açık İşler:** Üzerine tanımlı işler listesi
        - 📋 **Kullanıcı Yönetimi:** Kullanıcı bilgileri görüntüleme
        - ✅ **Onay Bekleyenler:** Aksiyonların sonuçlarını değerlendirip onaylama/reddetme
        """)

st.info("Sol üstteki menüden sayfalara geçiş yapabilirsin. Aksiyonlarını unutma 💡")

st.markdown("---")
st.caption("TEV | Burhan Özen (2025)")



