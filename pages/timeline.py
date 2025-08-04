# pages/timeline.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os

from config import KPI_DOSYA, KPI_SAYFA

def run():
    st.title("🗓️ KPI Zaman Çizelgesi (Timeline)")

    if not os.path.exists(KPI_DOSYA):
        st.error("KPI dosyası bulunamadı.")
        return

    df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)

    df_timeline = df[pd.notnull(df["Güncelleme Tarihi"])].copy()

    if df_timeline.empty:
        st.warning("Gösterilecek zaman çizelgesi yok.")
        return

    birimler = sorted(df_timeline["Faaliyet Sahibi Birim"].dropna().unique())
    birim_secimi = st.multiselect("📍 Birim Seçin", options=birimler, default=None)

    if birim_secimi:
        df_timeline = df_timeline[df_timeline["Faaliyet Sahibi Birim"].isin(birim_secimi)]

    if df_timeline.empty:
        st.warning("Seçilen birim(ler) için veri bulunamadı.")
        return

    fig = px.timeline(df_timeline,
                      x_start="Güncelleme Tarihi",
                      x_end="İlgili Faaliyet Başlangıç Tarihi",
                      y="Stratejik Hedef",
                      color="Durum",
                      title="KPI Süreç Zaman Çizelgesi")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
