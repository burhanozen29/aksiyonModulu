# pages/guncelleme_gecmisi.py

import streamlit as st
import pandas as pd
from io import BytesIO
import os

from config import LOG_DOSYA

def run():
    st.title("📜 Güncelleme Geçmişi")

    if not os.path.exists(LOG_DOSYA):
        st.warning("Henüz güncelleme yapılmamış veya log dosyası yok.")
        return

    df_log = pd.read_excel(LOG_DOSYA)

    # Tarih formatını düzelt
    if "Zaman" in df_log.columns:
        df_log["Zaman"] = pd.to_datetime(df_log["Zaman"])

    # Kullanıcı filtrelemesi (admin değilse sadece kendi kayıtları)
    if st.session_state.rol != "admin":
        df_log = df_log[df_log["Kullanıcı"] == st.session_state.kullanici]

    if df_log.empty:
        st.info("Gösterilecek kayıt yok.")
        return

    st.dataframe(df_log.sort_values(by="Zaman", ascending=False), use_container_width=True)

    # Excel indir
    with BytesIO() as buffer:
        df_log.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button("📥 Excel olarak indir", data=buffer, file_name="guncelleme_log.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Filtreleme
    st.subheader("🔍 Filtrele")

    kullanici_sec = st.multiselect("Kullanıcı", df_log["Kullanıcı"].unique())
    durum_sec = st.multiselect("Durum", df_log["Durum"].dropna().unique())

    df_filtreli = df_log.copy()
    if kullanici_sec:
        df_filtreli = df_filtreli[df_filtreli["Kullanıcı"].isin(kullanici_sec)]
    if durum_sec:
        df_filtreli = df_filtreli[df_filtreli["Durum"].isin(durum_sec)]

    if not df_filtreli.empty:
        st.dataframe(df_filtreli.sort_values(by="Zaman", ascending=False), use_container_width=True)
