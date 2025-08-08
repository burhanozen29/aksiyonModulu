# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:18:14 2025

@author: bozen
"""

# Sayfa 6: Kullanıcı Yönetimi
import streamlit as st
import pandas as pd
from aksiyon_kpi_modulu.database import tev_calisan
from pyvis.network import Network
import streamlit.components.v1 as components

if not st.session_state.get("giris_yapildi", False):
    st.warning("🔒 Bu sayfaya erişmek için önce giriş yapmalısınız.")
    st.stop()
st.title("👤 Kullanıcı Yönetimi")
if st.session_state.get("rol") != "admin":
    st.warning("Bu sayfaya sadece admin kullanıcılar erişebilir.")
    st.stop()
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


# ------------------------------
# Temizleme
# ------------------------------
def temizle(text):
    if text is None:
        return None
    return str(text).encode("utf-8", errors="ignore").decode("utf-8")

for col in ["İsim", "Bağlı Kişi", "Pozisyon (Yetki)", "Birim", "Mail"]:
    df_users[col] = df_users[col].apply(temizle)

# ------------------------------
# Zinciri çıkaran fonksiyon (yukarıya doğru)
# ------------------------------
def get_bagli_zincir(kisi, df):
    zincir = []
    while kisi is not None:
        zincir.insert(0, kisi)
        bagli_adi = kisi["Bağlı Kişi"]
        if bagli_adi and bagli_adi.strip() != "-":
            ust_kisi = df[df["İsim"] == bagli_adi]
            if not ust_kisi.empty:
                kisi = ust_kisi.iloc[0]
            else:
                break
        else:
            break
    return zincir

# ------------------------------
# Zinciri ekrana gösteren fonksiyon
# ------------------------------
def goster_kisi_chain(zincir):
    for kisi in zincir:
        isim = kisi["İsim"]
        pozisyon = kisi["Pozisyon (Yetki)"]
        birim = kisi["Birim"]
        mail = kisi["Mail"]

        with st.expander(f"{isim} ({pozisyon})", expanded=True):
            st.markdown(f"🏢 **Birim:** {birim}")
            st.markdown(f"📧 **E-posta:** {mail}")

# ------------------------------
# Uygulama arayüzü
# ------------------------------
st.title("👥 Organizasyon Hiyerarşisi")

arama = st.text_input("🔍 Kişi adıyla filtrele (Yazılmazsa tüm şema gösterilir)", "")

if arama.strip() == "":
    # Tüm yapı gösterilir
    st.info("Lütfen kişi adı yazarak filtreleme yapın.")
else:
    arama = arama.strip().lower()
    eslesenler = df_users[df_users["İsim"].str.lower().str.contains(arama)]

    if eslesenler.empty:
        st.warning("🚫 Eşleşen kişi bulunamadı.")
    else:
        st.success(f"🔎 {len(eslesenler)} eşleşme bulundu. Her biri için tıklayarak hiyerarşiyi görebilirsin.")
        for _, kisi in eslesenler.iterrows():
            zincir = get_bagli_zincir(kisi, df_users)
            with st.expander(f"🔽 {kisi['İsim']} ({kisi['Pozisyon (Yetki)']}) – Tıkla"):
                goster_kisi_chain(zincir)