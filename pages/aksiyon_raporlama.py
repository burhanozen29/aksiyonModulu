# pages/aksiyon_raporlama.py

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os

from config import KPI_DOSYA, KPI_SAYFA

def run():
    st.title("📊 Aksiyon / KPI Raporlama")

    if not os.path.exists(KPI_DOSYA):
        st.error("KPI dosyası bulunamadı.")
        return

    df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)

    # Admin değilse sadece kendi birimlerini görebilir
    kullanici_birimleri = df["Faaliyet Sahibi Birim"].dropna().unique()
    if st.session_state.rol != "admin":
        kullanici_birimleri = st.session_state.birimler

    birim_sec = st.multiselect("📌 Birim Seçin", options=sorted(kullanici_birimleri), default=None)

    durum_sec = st.multiselect("📂 Durum Seçin", options=sorted(df["Durum"].dropna().unique()), default=None)

    df_rapor = df.copy()
    if birim_sec:
        df_rapor = df_rapor[df_rapor["Faaliyet Sahibi Birim"].isin(birim_sec)]
    if durum_sec:
        df_rapor = df_rapor[df_rapor["Durum"].isin(durum_sec)]

    if df_rapor.empty:
        st.warning("Filtreye uygun veri bulunamadı.")
        return

    st.dataframe(df_rapor)

    # Excel export
    with BytesIO() as excel_io:
        df_rapor.to_excel(excel_io, index=False, engine='xlsxwriter')
        excel_io.seek(0)
        st.download_button("📥 Excel olarak indir", data=excel_io,
                           file_name="kpi_rapor.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.divider()

    # Durum sayımı grafiği
    durum_sayim = df_rapor["Durum"].value_counts().reset_index()
    durum_sayim.columns = ["Durum", "Adet"]

    fig1 = px.bar(durum_sayim,
                  x="Durum", y="Adet",
                  color="Durum",
                  color_discrete_map={
                      "Tamamlandı": "green",
                      "Tamamlanmadı": "red",
                      "Ertelendi": "blue",
                      "İptal Edildi": "gray"
                  },
                  title="Durum Bazlı KPI Dağılımı")
    st.plotly_chart(fig1)

    st.divider()

    fig2 = px.bar(df_rapor,
                  x="Faaliyet Sahibi Birim",
                  color="Durum",
                  barmode="stack",
                  title="Birimlere Göre Aksiyon Durumları")
    st.plotly_chart(fig2)
