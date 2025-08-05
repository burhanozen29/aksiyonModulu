# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:12:41 2025

@author: bozen
"""

# ui_main.py - Giriş ekranı ve yönlendirme
import streamlit as st
from aksiyon_kpi_modulu.auth import kullanici_dogrula

# === Oturum yönetimi ===
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False

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

