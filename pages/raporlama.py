# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:16:26 2025

@author: bozen
"""

# Sayfa 3: Raporlama ve görselleştirme
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os
from aksiyon_kpi_modulu.config import KPI_DOSYA, KPI_SAYFA

st.title("📈 KPI Raporlama ve Filtreleme")

if not os.path.exists(KPI_DOSYA):
    st.error("KPI dosyası bulunamadı.")
    st.stop()

df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)

# Kullanıcı yetkisine göre birimleri filtrele
kullanici_birimleri = st.session_state.birimler if st.session_state.rol != "admin" else df["Faaliyet Sahibi Birim"].dropna().unique()

birim_sec = st.multiselect(
    "📌 Birim Seçin",
    options=sorted(kullanici_birimleri),
    default=kullanici_birimleri if st.session_state.rol != "admin" else None,
    placeholder="Birim Seçin"
)

durum_sec = st.multiselect("📊 Durum Seçin", options=df["Durum"].dropna().unique(), placeholder="Durum Seçin")

df_rapor = df.copy()
if birim_sec:
    df_rapor = df_rapor[df_rapor["Faaliyet Sahibi Birim"].isin(birim_sec)]
if durum_sec:
    df_rapor = df_rapor[df_rapor["Durum"].isin(durum_sec)]

st.dataframe(df_rapor)

with BytesIO() as buffer:
    df_rapor.to_excel(buffer, index=False, engine='xlsxwriter')
    buffer.seek(0)
    st.download_button("📥 Excel olarak indir", data=buffer, file_name="kpi_rapor.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.divider()

if not df_rapor.empty:
    # Durum bazlı sayım
    durum_sayim = df_rapor["Durum"].value_counts().reset_index()
    durum_sayim.columns = ["Durum", "Adet"]
    renk_haritasi = {
        "Tamamlandı": "green",
        "Tamamlanmadı": "red",
        "Ertelendi": "blue",
        "İptal Edildi": "gray"
    }
    fig1 = px.bar(durum_sayim, x="Durum", y="Adet", color="Durum", color_discrete_map=renk_haritasi, title="Durum Bazlı KPI Sayısı")
    st.plotly_chart(fig1)

    st.divider()

    fig2 = px.bar(
        df_rapor,
        x="Faaliyet Sahibi Birim",
        color="Durum",
        barmode="stack",
        title="Birim Bazlı KPI Durum Dağılımı",
        category_orders={"Durum": ["Tamamlandı", "Tamamlanmadı", "İptal Edildi", "Ertelendi"]}
    )
    st.plotly_chart(fig2)
