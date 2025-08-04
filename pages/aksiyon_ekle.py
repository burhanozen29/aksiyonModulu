
# pages/aksiyon_ekle.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

from config import TEV_CALISAN, TEV_AKSIYON
from utils import aktif_ceyrek_bul

def run():
    st.title("🆕 Aksiyon Ekleme Paneli")

    def reset_modul():
        aksiyon_data = pd.DataFrame({
            "Modül": [modul_ekle],
            "İçerik": [modul_icerik],
            "Sorumlu Birim": [sorumlu_birim_sec],
            "Sorumlu Kişi": [sorumlu_kisi_sec],
            "İşi Yapacak Birim": [isi_yapacak_birim_sec],
            "İşi Yapacak Kişi": [isi_yapacak_kisi_sec],
            "Ölçü Birimi": [olcu_ekle],
            "Referans Değeri": [refDeger],
            "MinMax": [minMax],
            "Termin Tarihi": [terminTarihi],
            "Aksiyon Ekleme Tarihi": datetime.now()
        })

        if os.path.exists(TEV_AKSIYON):
            mevcut_df = pd.read_excel(TEV_AKSIYON)
            guncel_df = pd.concat([mevcut_df, aksiyon_data], ignore_index=True)
        else:
            guncel_df = aksiyon_data

        guncel_df.to_excel(TEV_AKSIYON, index=False)
        st.success("✅ Aksiyon başarıyla eklendi!")
        time.sleep(1)
        st.rerun()

    moduller = ["Süreç Kararları", "Toplantı Kararları", "Diğer Kararlar"]
    modul_ekle = st.selectbox("Modül Seç", options=moduller, index=None)

    if modul_ekle:
        modul_icerik = st.text_area(f"{modul_ekle} içeriğini girin")
        if modul_icerik:
            kullanıcılar = pd.read_excel(TEV_CALISAN)
            sorumlu_kullanıcılar = kullanıcılar[kullanıcılar["Bağlı Kişi Birim"].isin(["-", "Genel Müdürlük"]) == False]
            sorumlu_birim_sec = st.selectbox("Sorumlu Birim", sorted(sorumlu_kullanıcılar["Birim"].unique()), index=None)
            
            if sorumlu_birim_sec:
                sorumlu_kisi_sec = st.selectbox("Sorumlu Kişi",
                                                options=sorumlu_kullanıcılar[sorumlu_kullanıcılar["Birim"] == sorumlu_birim_sec]["İsim"],
                                                index=None)
                if sorumlu_kisi_sec:
                    isi_yapacak_birim_sec = st.selectbox("İşi Yapacak Birim", sorted(kullanıcılar["Birim"].unique()), index=None)
                    if isi_yapacak_birim_sec:
                        isi_yapacak_kisi_sec = st.selectbox("İşi Yapacak Kişi",
                                                            options=kullanıcılar[kullanıcılar["Birim"] == isi_yapacak_birim_sec]["İsim"],
                                                            index=None)
                        if isi_yapacak_kisi_sec:
                            olcu_birimleri = ["Oran", "Sayı"]
                            olcu_ekle = st.selectbox("Ölçü Birimi", options=olcu_birimleri, index=None)

                            if olcu_ekle:
                                minMax = st.radio("Referans Yönü", ["En Az", "En Çok"], horizontal=True)
                                if minMax:
                                    if olcu_ekle == "Oran":
                                        refDeger = st.number_input("Referans Değeri (%)", min_value=0.0, max_value=100.0, step=0.1) / 100
                                    else:
                                        refDeger = st.number_input("Referans Değeri", min_value=0, max_value=1000, step=1)

                                    terminTarihi = st.date_input("Termin Tarihi", value=datetime.today(), min_value=datetime.today())

                                    if st.button("📌 Aksiyonu Kaydet"):
                                        reset_modul()
