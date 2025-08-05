# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:18:47 2025

@author: bozen
"""

# Sayfa 7: Açık İşler
import streamlit as st
import pandas as pd
import os
from aksiyon_kpi_modulu.config import TEV_AKSIYON

st.title("📋 Üzerine Tanımlı Aksiyonlar")
select, compare = st.tabs(["Açık İşler", "Tüm İşler"])

if not os.path.exists(TEV_AKSIYON):
    st.warning("Aksiyonlar dosyası bulunamadı.")
    st.stop()

with select:
    st.subheader("🚧 Açık Aksiyonlar")
    df = pd.read_excel(TEV_AKSIYON)
    df = df[df["İşi Yapacak Birim"] == st.session_state.birimler[0]]
    df = df[~df["Yapıldı Mı"].isin(["Evet", "Hayır"])]
    st.dataframe(df, use_container_width=True)

with compare:
    st.subheader("📋 Tüm Aksiyonlar")
    df_all = pd.read_excel(TEV_AKSIYON)
    df_all = df_all[df_all["İşi Yapacak Birim"] == st.session_state.birimler[0]]
    st.dataframe(df_all, use_container_width=True)
