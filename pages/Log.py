# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:17:36 2025

@author: bozen
"""

# Sayfa 5: Güncelleme Geçmişi (Log)
import streamlit as st
import pandas as pd
import os
from io import BytesIO
from aksiyon_kpi_modulu.config import LOG_DOSYA

if not st.session_state.get("giris_yapildi", False):
    st.warning("🔒 Bu sayfaya erişmek için önce giriş yapmalısınız.")
    st.stop()
st.title("🕓 Aksiyon Log Kayıtları")
if st.session_state.get("rol") != "admin":
    st.warning("Bu sayfaya sadece admin kullanıcılar erişebilir.")
    st.stop()
if os.path.exists(LOG_DOSYA):
    log_df = pd.read_excel(LOG_DOSYA)
    st.dataframe(log_df.sort_index(ascending=False))

    with st.expander("⬇️ Excel olarak indir"):
        buffer = BytesIO()
        log_df.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="📥 İndir",
            data=buffer,
            file_name="log_kpi_guncelleme.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Henüz hiç log kaydı bulunmamaktadır.")
