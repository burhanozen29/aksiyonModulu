# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:14:29 2025

@author: bozen
"""

# Sayfa 1: Aksiyon Ekleme modülü
import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from aksiyon_kpi_modulu.database import tev_calisan
from aksiyon_kpi_modulu.config import TEV_AKSIYON

st.title("📝 Aksiyon Ekleme Paneli")

def reset_modul():
    aksiyon_data = pd.DataFrame({
        "Modül": [modul_ekle],
        "İçerik": [modul_icerik],
        "Sorumlu Birim" : [sorumlu_birim_sec],
        "Sorumlu Kişi" : [sorumlu_kisi_sec],
        "İşi Yapacak Birim" : [isi_yapacak_birim_sec],
        "İşi Yapacak Kişi" : [isi_yapacak_kisi_sec],
        "Ölçü Birimi" : [olcu_ekle],
        "Referans Değeri":[refDeger],
        "MinMax":[minMax],
        "Termin Tarihi":[terminTarihi],
        "Aksiyon Ekleme Tarihi":datetime.now()
    })

    if os.path.exists(TEV_AKSIYON):
        mevcut_df = pd.read_excel(TEV_AKSIYON)
        guncel_df = pd.concat([mevcut_df, aksiyon_data], ignore_index=True)
    else:
        guncel_df = aksiyon_data

    guncel_df.to_excel(TEV_AKSIYON, index=False)
    st.success("✅ Veri başarıyla eklendi!")
    time.sleep(2)
    st.session_state.clear()

moduller = ["Süreç Kararları","Toplantı Kararları","Diğer Kararlar"]
modul_ekle = st.selectbox("Modül Seç", options=moduller, index=None, key="modul")

if modul_ekle:
    modul_icerik = st.text_area(f"{modul_ekle} içeriğini girin", key="içerik")
    if modul_icerik:
        veriler = list(tev_calisan.find())
        kullanıcılar = pd.DataFrame(veriler)
        sorumlu_kullanıcılar = kullanıcılar[kullanıcılar["Bağlı Kişi Birim"].isin(["-", "Genel Müdürlük"]) == False]
        sorumlu_birim_sec = st.selectbox("Sorumlu Birim Seç", options=sorumlu_kullanıcılar["Birim"].unique(), index=None, key="sorumluBirim")

        if sorumlu_birim_sec:
            sorumlu_kisi_sec = st.selectbox("Sorumlu Kişi Seç", options=sorumlu_kullanıcılar[sorumlu_kullanıcılar["Birim"] == sorumlu_birim_sec]["İsim"], index=None, key="sorumluKişi")
            if sorumlu_kisi_sec:
                isi_yapacak_birim_sec = st.selectbox("İşi Yapacak Birim Seç", options=kullanıcılar["Birim"].unique(), index=None, key="işiYapacakBirim")
                if isi_yapacak_birim_sec:
                    isi_yapacak_kisi_sec = st.selectbox("İşi Yapacak Kişi Seç", options=kullanıcılar[kullanıcılar["Birim"] == isi_yapacak_birim_sec]["İsim"], index=None, key="işiYapacakKişi")
                    if isi_yapacak_kisi_sec:
                        olcu_birimi = ["Oran","Sayı"]
                        olcu_ekle = st.selectbox("Ölçü Birimi Ekle", options=olcu_birimi, index=None, key="ölçüTipi")
                        if olcu_ekle:
                            minMax = st.radio("Referans Değeri Sınırı", ["En Az","En Çok"], horizontal=True, index=None, key="minMax")
                            if minMax:
                                if olcu_ekle == "Oran":
                                    refDeger = st.number_input("Referans değeri (0-100%)", min_value=0.0, max_value=100.0, step=0.1, key="referans") / 100
                                else:
                                    refDeger = st.number_input("Referans değeri", min_value=0, max_value=1000, step=1, key="referans")
                                terminTarihi = st.date_input("Termin Tarihi Girin", value=datetime.today(), min_value=datetime.today(), key="termin_tarihi")
                                if terminTarihi:
                                    st.button("📌 Aksiyon Ekle", on_click=reset_modul)

