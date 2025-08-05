# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:15:11 2025

@author: bozen
"""

# Sayfa 2: Aksiyon Güncelleme (taslak başlangıç)
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from aksiyon_kpi_modulu.config import KPI_DOSYA, KPI_SAYFA, TEV_AKSIYON, KANIT_KLASORU, LOG_DOSYA
from aksiyon_kpi_modulu.utils import aktif_ceyrek_bul

st.title("📊 Aksiyon Güncelleme Paneli")

moduller = ["Süreç Kararları","Toplantı Kararları","Diğer Kararlar","KPI"]
modul_sec = st.selectbox("Modül Seç", options=moduller, index=None)

if modul_sec == "KPI":
    if not os.path.exists(KPI_DOSYA):
        st.error("KPI dosyası bulunamadı.")
        st.stop()

    df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)
    birim = st.session_state.birimler[0] if st.session_state.rol != "admin" else None
    if birim:
        df = df[df["Faaliyet Sahibi Birim"] == birim]

    aktif_ceyrek = "Hedef " + aktif_ceyrek_bul()
    ana_stratejiler = df[df[aktif_ceyrek].notna()]["Ana Strateji"].dropna().unique()
    ana_strateji = st.selectbox("1️⃣ Ana Strateji", options=sorted(ana_stratejiler), index=None)

    if ana_strateji:
        df_amac = df[df["Ana Strateji"] == ana_strateji]
        stratejik_amac = st.selectbox("2️⃣ Stratejik Amaç", options=sorted(df_amac["Stratejik Amaç"].dropna().unique()), index=None)
        if stratejik_amac:
            df_hedef = df_amac[df_amac["Stratejik Amaç"] == stratejik_amac]
            stratejik_hedef = st.selectbox("3️⃣ Stratejik Hedef", options=sorted(df_hedef["Stratejik Hedef"].dropna().unique()), index=None)
            if stratejik_hedef:
                df_faaliyet = df_hedef[df_hedef["Stratejik Hedef"] == stratejik_hedef]
                selected_kpi = st.selectbox("4️⃣ Faaliyet", options=sorted(df_faaliyet["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"].dropna().unique()), index=None)

                if selected_kpi:
                    kpi_row_idx = df[df["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"] == selected_kpi].index[0]
                    refDegerHedef = float(df.at[kpi_row_idx, aktif_ceyrek])
                    refDegerStr = df.at[kpi_row_idx, 'Hedef Ölçüsü']
                    refDeger = st.number_input("Gerçekleşen Değer", min_value=0.0, max_value=1.0 if refDegerStr == "Oran" else 100.0, step=0.01)

                    durum = "Tamamlandı" if refDeger >= refDegerHedef else st.selectbox("Durum", ["Tamamlanmadı", "Ertelendi", "İptal Edildi"])
                    aciklama = st.text_area("Açıklama / Gerekçe")
                    yeni_tarih = st.date_input("Yeni hedef tarih", value=datetime.today())

                    uploaded_file = st.file_uploader("📎 Kanıt Belgesi (ZORUNLU)", type=["pdf", "docx", "xlsx", "csv", "xls"])
                    if st.button("📩 Güncelle ve Kaydet"):
                        if not uploaded_file:
                            st.error("❗ Lütfen zorunlu dosyayı yükleyin!")
                        else:
                            os.makedirs(KANIT_KLASORU, exist_ok=True)
                            file_path = os.path.join(KANIT_KLASORU, uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.read())

                            df.at[kpi_row_idx, "Durum"] = durum
                            df.at[kpi_row_idx, "Açıklama"] = aciklama
                            df.at[kpi_row_idx, "Önerilen Yeni Tarih"] = yeni_tarih.strftime("%Y-%m-%d")
                            df.at[kpi_row_idx, "Güncelleme Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            df.at[kpi_row_idx, "Kanıt"] = uploaded_file.name
                            df.to_excel(KPI_DOSYA, sheet_name=KPI_SAYFA, index=False)

                            st.success("✅ Güncelleme kaydedildi.")
