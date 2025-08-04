# pages/aksiyon_guncelle.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

from config import KPI_DOSYA, KPI_SAYFA, KANIT_KLASORU, TEV_AKSIYON, TEV_CALISAN, LOG_DOSYA
from utils import aktif_ceyrek_bul

def run():
    st.title("📝 Aksiyon Güncelleme Paneli")

    if not os.path.exists(KPI_DOSYA):
        st.error("KPI dosyası bulunamadı.")
        return

    df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)

    # Rol bazlı filtreleme
    if st.session_state.rol != "admin":
        df = df[df["Faaliyet Sahibi Birim"].isin(st.session_state.birimler)]

    if df.empty:
        st.warning("Görüntülenecek veri bulunamadı.")
        return

    aktif_ceyrek = "Hedef " + aktif_ceyrek_bul()

    moduller = ["KPI", "Süreç Kararları", "Toplantı Kararları", "Diğer Kararlar"]
    modul_sec = st.selectbox("Modül Seç", options=moduller, index=None)

    # === KPI GÜNCELLEME ===
    if modul_sec == "KPI":
        ana_stratejiler = sorted(df.loc[df[aktif_ceyrek].notna(), "Ana Strateji"].dropna().unique())
        ana_strateji = st.selectbox("Ana Strateji", options=ana_stratejiler, index=None)

        if not ana_strateji:
            return

        df_amac = df[(df["Ana Strateji"] == ana_strateji) & (df[aktif_ceyrek].notna())]
        stratejik_amac = st.selectbox("Stratejik Amaç", sorted(df_amac["Stratejik Amaç"].dropna().unique()), index=None)

        if not stratejik_amac:
            return

        df_hedef = df_amac[df_amac["Stratejik Amaç"] == stratejik_amac]
        stratejik_hedef = st.selectbox("Stratejik Hedef", sorted(df_hedef["Stratejik Hedef"].dropna().unique()), index=None)

        if not stratejik_hedef:
            return

        df_faaliyet = df_hedef[df_hedef["Stratejik Hedef"] == stratejik_hedef]
        secilen_kpi = st.selectbox("Faaliyet", sorted(df_faaliyet["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"].dropna().unique()), index=None)

        if not secilen_kpi:
            return

        idx = df[df["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"] == secilen_kpi].index[0]

        ref_deger = float(df.at[idx, aktif_ceyrek])
        ref_tip = df.at[idx, "Hedef Ölçüsü"]

        st.subheader("📤 Güncelleme Formu")

        if ref_tip.lower() in ["oran", "yüzde"]:
            girilen_deger = st.number_input("Gerçekleşen Değer (%)", 0.0, 1.0, step=0.01)
        else:
            girilen_deger = st.number_input("Gerçekleşen Değer", 0.0, 1000.0, step=1.0)

        if girilen_deger < ref_deger:
            durum = st.selectbox("Durum", ["Tamamlanmadı", "Ertelendi", "İptal Edildi"])
        else:
            durum = "Tamamlandı"
            st.text_input("Durum", value=durum, disabled=True)

        aciklama = st.text_area("Açıklama / Gerekçe")

        yeni_tarih_gir = st.checkbox("📅 Yeni hedef tarihi girmek istiyorum")
        if yeni_tarih_gir:
            yeni_tarih = st.date_input("Yeni Tarih", min_value=datetime.today())
        else:
            yeni_tarih = None

        st.markdown('<p style="color:red; font-weight:bold;">📎 Kanıt Belgesi (Zorunlu)</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Belge yükleyin", type=["pdf", "xlsx", "docx", "jpg", "png"])

        if st.button("💾 Güncellemeyi Kaydet"):
            if uploaded_file is None:
                st.error("Lütfen zorunlu belgeyi yükleyin.")
                return

            # Belge kaydı
            os.makedirs(KANIT_KLASORU, exist_ok=True)
            belge_yolu = os.path.join(KANIT_KLASORU, uploaded_file.name)
            with open(belge_yolu, "wb") as f:
                f.write(uploaded_file.read())

            df.at[idx, "Durum"] = durum
            df.at[idx, "Açıklama"] = aciklama
            df.at[idx, "Kanıt"] = uploaded_file.name
            df.at[idx, "Güncelleme Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if yeni_tarih:
                df.at[idx, "Önerilen Yeni Tarih"] = yeni_tarih.strftime("%Y-%m-%d")

            df.to_excel(KPI_DOSYA, sheet_name=KPI_SAYFA, index=False)

            # Log kaydı
            log_kaydi = {
                "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Kullanıcı": st.session_state.kullanici,
                "KPI Adı": secilen_kpi,
                "Durum": durum,
                "Açıklama": aciklama,
                "Yeni Tarih": yeni_tarih.strftime("%Y-%m-%d") if yeni_tarih else "",
                "Yüklenen Dosya": uploaded_file.name
            }

            log_df = pd.DataFrame([log_kaydi])
            if os.path.exists(LOG_DOSYA):
                mevcut_log = pd.read_excel(LOG_DOSYA)
                tum_log = pd.concat([mevcut_log, log_df], ignore_index=True)
            else:
                tum_log = log_df

            tum_log.to_excel(LOG_DOSYA, index=False)

            st.success("✅ Güncelleme ve log başarıyla kaydedildi!")

    # === SÜREÇ/TOPLANTI AKSİYONLARI ===
    elif modul_sec in ["Süreç Kararları", "Toplantı Kararları", "Diğer Kararlar"]:
        st.info("Bu modülün güncelleme ekranı henüz tamamlanmadı.")
