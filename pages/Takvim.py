# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:17:15 2025

@author: bozen
"""

# Sayfa 4: KPI Takvim Görünümü 
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from aksiyon_kpi_modulu.config import KPI_DOSYA, KPI_SAYFA

if not st.session_state.get("giris_yapildi", False):
    st.warning("🔒 Bu sayfaya erişmek için önce giriş yapmalısınız.")
    st.stop()
st.title("🗓️ KPI Takvim / Timeline Görünümü")

if not os.path.exists(KPI_DOSYA):
    st.error("KPI dosyası bulunamadı.")
    st.stop()

df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)

birim_secimi = st.multiselect(
    "📌 Birim",
    options=sorted(df["Faaliyet Sahibi Birim"].dropna().unique()),
    default=None,
    placeholder="Birim(leri) Seçin (Seçim yapmazsanız tümü gösterilir)"
)

df_timeline = df[pd.notnull(df["Güncelleme Tarihi"])].copy()

if birim_secimi:
    df_timeline = df_timeline[df_timeline["Faaliyet Sahibi Birim"].isin(birim_secimi)]

if df_timeline.empty:
    st.warning("Gösterilecek zaman çizelgesi bulunamadı.")
else:
    fig = px.timeline(
        df_timeline,
        x_start="Güncelleme Tarihi",
        x_end="İlgili Faaliyet Başlangıç Tarihi",
        y="Stratejik Hedef",
        color="Durum",
        title="KPI Süreç Takvimi"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
