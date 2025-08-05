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

if not st.session_state.get("giris_yapildi", False):
    st.warning("🔒 Bu sayfaya erişmek için önce giriş yapmalısınız.")
    st.stop()
st.title("📈 KPI Raporlama ve Filtreleme")

if not os.path.exists(KPI_DOSYA):
    st.error("KPI dosyası bulunamadı.")
    st.stop()

df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)

kullanici_birimleri = st.session_state.birimler if st.session_state.rol != "admin" else df["Faaliyet Sahibi Birim"].dropna().unique()

birim_sec = st.multiselect(
    "Birim",
    options=sorted(kullanici_birimleri),
    default=kullanici_birimleri if st.session_state.rol != "admin" else None,
    placeholder="Birim Seçin"
)

durum_sec = st.multiselect("Durum", options=df["Durum"].dropna().unique(),
                           default=None,
                           placeholder="Durum Seçin")

df_rapor = df[df["Faaliyet Sahibi Birim"].isin(birim_sec)] if birim_sec else df.copy()

if durum_sec:
    df_rapor = df_rapor[df_rapor["Durum"].isin(durum_sec)]

st.dataframe(df_rapor)

# Excel Dışa Aktarım
with BytesIO() as excel_io:
    df_rapor.to_excel(excel_io, index=False, engine='xlsxwriter')
    excel_io.seek(0)
    st.download_button("📥 Excel olarak indir", data=excel_io,
                        file_name="kpi_rapor.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.divider()
    
if not df_rapor.empty:
    durum_sayim = df_rapor["Durum"].value_counts().reset_index()
    durum_sayim.columns = ["Durum", "Adet"]
    renk_haritasi = {
        "Tamamlandı":"green",
        "Tamamlanmadı":"red",
        "Ertelendi":"blue",
        "İptal Edildi":"gray"
        }
    fig = px.bar(durum_sayim,
                 x="Durum",
                 y="Adet", 
                 color="Durum",
                 color_discrete_map=renk_haritasi,
                 title="Durum Bazlı KPI Sayısı")
    st.plotly_chart(fig)
    
    st.divider()
    
    fig = px.bar(
        df_rapor,
        x="Faaliyet Sahibi Birim",
        color="Durum",
        title="Faaliyet Sahibi Birime Göre Durum Dağılımı",
        barmode="stack",
        category_orders={"Durum": ["Tamamlandı", "Tamamlanmadı", "İptal Edildi","Ertelendi"]}  # İstersen durum sırasını buraya yazabilirsin
    )
    
    st.plotly_chart(fig)

        
st.stop()