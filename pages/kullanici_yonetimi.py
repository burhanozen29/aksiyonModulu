# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:18:14 2025

@author: bozen
"""

# Sayfa 6: Kullanıcı Yönetimi
import streamlit as st
import pandas as pd
from aksiyon_kpi_modulu.database import tev_calisan

st.title("👤 Kullanıcı Yönetimi")

veriler = list(tev_calisan.find())
df_users = pd.DataFrame(veriler)

show_password = st.checkbox("🔓 Şifreyi Göster", value=False)

if show_password:
    st.dataframe(df_users)
else:
    df_masked = df_users.copy()
    if "Şifre" in df_masked.columns:
        df_masked["Şifre"] = df_masked["Şifre"].apply(lambda x: "*" * len(str(x)) if pd.notna(x) else "")
    st.dataframe(df_masked)
