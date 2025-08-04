# pages/kullanici_yonetimi.py

import streamlit as st
import pandas as pd
import os
import time

from config import KULLANICI_DOSYA, TEV_CALISAN

def run():
    st.title("👤 Kullanıcı Yönetimi")

    # Kullanıcı dosyasını oku veya oluştur
    if os.path.exists(KULLANICI_DOSYA):
        df_users = pd.read_excel(KULLANICI_DOSYA)
    else:
        df_users = pd.DataFrame(columns=["Kullanıcı Adı", "Şifre", "Birimler", "Rol"])

    mevcut_kullanicilar = sorted(df_users["Kullanıcı Adı"].dropna().unique())

    # Yeni kullanıcı ekleme / güncelleme
    st.subheader("➕ Kullanıcı Ekle / Güncelle")

    yeni_kullanici = st.text_input("Kullanıcı Adı")
    yeni_sifre = st.text_input("Şifre", type="password")
    birimler = sorted(df_users["Birimler"].str.split(",").explode().dropna().unique())
    secilen_birimler = st.multiselect("Birim(ler)", options=birimler)
    yeni_rol = st.selectbox("Rol", ["admin", "kullanıcı"], index=0)

    if st.button("💾 Kaydet"):
        if not (yeni_kullanici and yeni_sifre and secilen_birimler and yeni_rol):
            st.warning("Tüm alanları doldurun.")
        else:
            yeni_kayit = {
                "Kullanıcı Adı": yeni_kullanici,
                "Şifre": yeni_sifre,
                "Birimler": ",".join(secilen_birimler),
                "Rol": yeni_rol
            }

            if yeni_kullanici in df_users["Kullanıcı Adı"].values:
                df_users.loc[df_users["Kullanıcı Adı"] == yeni_kullanici, ["Şifre", "Birimler", "Rol"]] = (
                    yeni_sifre, ",".join(secilen_birimler), yeni_rol
                )
                st.success("✅ Kullanıcı güncellendi.")
            else:
                df_users = pd.concat([df_users, pd.DataFrame([yeni_kayit])], ignore_index=True)
                st.success("✅ Yeni kullanıcı eklendi.")

            df_users.to_excel(KULLANICI_DOSYA, index=False)
            time.sleep(1)
            st.rerun()

    st.divider()

    # Kullanıcı silme
    st.subheader("❌ Kullanıcı Sil")

    silinecek_kullanici = st.selectbox("Silinecek Kullanıcı", options=mevcut_kullanicilar, index=None)

    if st.button("🗑️ Sil"):
        if not silinecek_kullanici:
            st.warning("Silinecek kullanıcıyı seçmelisiniz.")
        else:
            df_users = df_users[df_users["Kullanıcı Adı"] != silinecek_kullanici]
            df_users.to_excel(KULLANICI_DOSYA, index=False)
            st.success("🚫 Kullanıcı silindi.")
            time.sleep(1)
            st.rerun()

    st.divider()

    # Şifreyi göster/gizle
    show_pw = st.checkbox("🔐 Şifreleri Göster")

    if show_pw:
        st.dataframe(df_users)
    else:
        df_masked = df_users.copy()
        df_masked["Şifre"] = df_masked["Şifre"].apply(lambda x: "*" * len(str(x)))
        st.dataframe(df_masked)

    # TEV çalışan listesi varsa göster
    if os.path.exists(TEV_CALISAN):
        df_calisan = pd.read_excel(TEV_CALISAN)
        st.subheader("📋 TEV Çalışanları")
        st.dataframe(df_calisan)
