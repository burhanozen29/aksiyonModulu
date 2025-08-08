# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 23:24:20 2025

@author: bozen
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from aksiyon_kpi_modulu.config import TEV_AKSIYON, LOG_DOSYA
import os

st.set_page_config(page_title="Onay Bekleyenler", page_icon="✅", layout="wide")

# === Giriş kontrolü ===
if not st.session_state.get("giris_yapildi", False):
    st.warning("🔒 Bu sayfaya erişmek için önce giriş yapmalısınız.")
    st.stop()

kullanici = st.session_state.get("kullanici")
isim = st.session_state.get("isim")

# === MongoDB bağlantısı (bağlı kişileri bulmak için) ===
client = MongoClient("mongodb://localhost:27017/")
db = client["aksiyon_modul"]
tev_calisan = pd.DataFrame(list(db["tev_calisan"].find()))

# Giriş yapan kişinin bağlı olduğu kişiler
baglilar = tev_calisan[tev_calisan["Bağlı Kişi"] == isim]["İsim"].tolist()


if not baglilar:
    st.info("📭 Size bağlı personel bulunmamaktadır.")
    st.stop()

# === Aksiyonlar dosyasını oku ===
try:
    df = pd.read_excel(TEV_AKSIYON)
except FileNotFoundError:
    st.error("Aksiyonlar dosyası bulunamadı.")
    st.stop()

# Onay bekleyenleri filtrele
df_onay = df[
    (df["İşi Yapacak Kişi"].isin(baglilar)) &
    (df["Onay"].eq("Onay Bekliyor")) & 
     df["Yeni Tarih Talebi"].fillna("").eq("")
].copy()

df_tarih = df[
    (df["İşi Yapacak Kişi"].isin(baglilar)) &
    (df["Yeni Tarih Talebi"].eq("Onay Bekliyor"))
    ].copy()

if df_onay.empty and df_tarih.empty:
    st.info("📬 Şu anda onay bekleyen bir aksiyon bulunmamaktadır.")
    st.stop()

st.title("📝 Onay Bekleyen Aksiyonlar")
st.markdown(f"**👤 Kullanıcı:** `{isim}`")
st.markdown("---")


select, compare = st.tabs(["Aksiyon Onayları", "Yeni Tarih Önerileri"])
with select:
    for i, row in df_onay.iterrows():
        st.subheader(f"📌 {row['İçerik']}")
        durum = row["Durum"]
        sorumlu = row["İşi Yapacak Kişi"]
        aciklama = row["Açıklama"]
        termin = row["Termin Tarihi"].strftime('%d.%m.%Y') if pd.notna(row["Termin Tarihi"]) else "Belirtilmemiş"
        
        if "Tamamlandı" in durum:
            renk = "#d4edda"  # açık yeşil
            cerceve = "#155724"
        elif "Tamamlanmadı" in durum:
            renk = "#e2e3e5"  # açık gri
            cerceve = "#383d41"
        else:
            renk = "#fff3cd"  # sarımsı uyarı
            cerceve = "#856404"
        
        st.markdown(f"""
        <div style="background-color:{renk}; border-left: 5px solid {cerceve}; padding: 10px; margin-bottom: 10px; border-radius: 4px;">
            <b>Durum:</b> {durum}<br>
            <b>Sorumlu:</b> {sorumlu}<br>
            <b>Termin Tarihi:</b> {termin} <br>
            <b>Girilen Açıklama:</b> {aciklama}
        </div>
        """, unsafe_allow_html=True)
        if pd.notna(row.get("Kanıt")):
            dosya_adi = row["Kanıt"]
            dosya_yolu = f"kanitlar/{dosya_adi}"  # klasör içinde
        
            if os.path.exists(dosya_yolu):
                if dosya_adi.lower().endswith(".pdf"):
                    with st.expander("📎 Aksiyonun Tamamlanma Kanıt Dosyasını Görüntüle (PDF)"):
                        with open(dosya_yolu, "rb") as f:
                            import base64
                            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                            pdf_viewer = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500px"></iframe>'
                            st.markdown(pdf_viewer, unsafe_allow_html=True)
                else:
                    with open(dosya_yolu, "rb") as f:
                        st.download_button(
                            label="📎 Aksiyonun Tamamlanma Kanıt Dosyasını İndir",
                            data=f,
                            file_name=dosya_adi,
                            mime="application/octet-stream",
                            key = f"download_{i}"
                        )
            else:
                st.warning(f"❗ Kanıt dosyası bulunamadı: `{dosya_adi}`")
            
    
        onay_aciklama = st.text_area("Açıklama (Zorunlu)", key=f"aciklama_{i}")
        if onay_aciklama:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Onayla", key=f"onayla_{i}"):
                    df.at[i, "Durum"] = row["Durum"]
                    df.at[i, "Onay"] = "Onaylandı"
                    df.at[i, "Yeni Tarih Talebi"] = ""
                    df.at[i, "Onaylayan"] = isim
                    df.at[i, "Onay Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df.at[i, "Onay Açıklaması"] = onay_aciklama
                    df.to_excel(TEV_AKSIYON, index=False)
                    
                    
                    log_df = pd.read_excel(LOG_DOSYA)
                    yeni_log = pd.DataFrame([{
                        "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Kullanıcı": st.session_state.get("isim"),
                        "Aksiyon": row["İçerik"],
                        "Durum": row["Durum"],
                        "Onay":"Onaylandı",
                        "Yeni Tarih Talebi":"",
                        "Açıklama": onay_aciklama,
                        "Aşama":"Onay İşlemleri"
                    }])
                    log_df = pd.concat([log_df, yeni_log], ignore_index=True)
                    log_df.to_excel(LOG_DOSYA, index=False)
                    
                    st.success("✅ Onaylandı ve kayıt güncellendi.")
                    st.rerun()
            with col2:
                if st.button("❌ Reddet", key=f"reddet_{i}"):
                    df.at[i, "Durum"] = row["Durum"]
                    df.at[i, "Onay"] = "Reddedildi"
                    df.at[i, "Yeni Tarih Talebi"] = ""
                    df.at[i, "Onaylayan"] = isim
                    df.at[i, "Onay Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df.at[i, "Onay Açıklaması"] = onay_aciklama
                    df.to_excel(TEV_AKSIYON, index=False)
                    
                    
                    
                    log_df = pd.read_excel(LOG_DOSYA)
                    yeni_log = pd.DataFrame([{
                        "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Kullanıcı": st.session_state.get("isim"),
                        "Aksiyon": row["İçerik"],
                        "Durum":row["Durum"],
                        "Onay": "Reddedildi",
                        "Yeni Tarih Talebi":"",
                        "Açıklama": onay_aciklama,
                        "Aşama":"Onay İşlemleri"
                    }])
                    log_df = pd.concat([log_df, yeni_log], ignore_index=True)
                    log_df.to_excel(LOG_DOSYA, index=False)
                    
                    
                    st.warning("❌ Aksiyon reddedildi.")
                    st.rerun()
        st.markdown('<div style="height:2px;background:#ccc;margin:20px 0;"></div>', unsafe_allow_html=True)
    
with compare:
    for i, row in df_tarih.iterrows():
        
        st.subheader(f"📌 {row['İçerik']}")
        durum = row["Durum"]
        sorumlu = row["İşi Yapacak Kişi"]
        aciklama = row["Açıklama"]
        yeni_tarih = row["Yeni Tarih"].strftime('%d.%m.%Y')
        termin = row["Termin Tarihi"].strftime('%d.%m.%Y') if pd.notna(row["Termin Tarihi"]) else "Belirtilmemiş"
        
        if "Tamamlandı" in durum:
            renk = "#d4edda"  # açık yeşil
            cerceve = "#155724"
        elif "Tamamlanmadı" in durum:
            renk = "#e2e3e5"  # açık gri
            cerceve = "#383d41"
        else:
            renk = "#fff3cd"  # sarımsı uyarı
            cerceve = "#856404"
        
        st.markdown(f"""
        <div style="background-color:{renk}; border-left: 5px solid {cerceve}; padding: 10px; margin-bottom: 10px; border-radius: 4px;">
            <b>Durum:</b> {durum}<br>
            <b>Sorumlu:</b> {sorumlu}<br>
            <b>Termin Tarihi:</b> {termin} <br>
            <b>Girilen Açıklama:</b> {aciklama} <br>
            <b>Yeni Tarih Önerisi: {yeni_tarih} </b>
        </div>
        """, unsafe_allow_html=True)
        if pd.notna(row.get("Kanıt")):
            dosya_adi = row["Kanıt"]
            dosya_yolu = f"kanitlar/{dosya_adi}"  # klasör içinde
        
            if os.path.exists(dosya_yolu):
                if dosya_adi.lower().endswith(".pdf"):
                    with st.expander("📎 Aksiyonun Tamamlanma Kanıt Dosyasını Görüntüle (PDF)"):
                        with open(dosya_yolu, "rb") as f:
                            import base64
                            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                            pdf_viewer = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500px"></iframe>'
                            st.markdown(pdf_viewer, unsafe_allow_html=True)
                else:
                    with open(dosya_yolu, "rb") as f:
                        st.download_button(
                            label="📎 Aksiyonun Tamamlanma Kanıt Dosyasını İndir",
                            data=f,
                            file_name=dosya_adi,
                            mime="application/octet-stream",
                            key = f"download_{i}"
                        )
            else:
                st.warning(f"❗ Kanıt dosyası bulunamadı: `{dosya_adi}`")
            
    
        onay_aciklama = st.text_area("Açıklama (Zorunlu)", key=f"aciklama_{i}")
        if onay_aciklama:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Onayla", key=f"onayla_{i}"):
                    df.at[i, "Durum"] = "Aksiyon Bekleniyor"
                    df.at[i, "Onay"] = ""
                    df.at[i, "Yeni Tarih Talebi"] = "Onaylandı"
                    df.at[i, "Onaylayan"] = isim
                    df.at[i, "Onay Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df.at[i, "Onay Açıklaması"] = onay_aciklama
                    df.at[i, "Termin Tarihi"] = yeni_tarih
                    df.to_excel(TEV_AKSIYON, index=False)
                    
                    
                    log_df = pd.read_excel(LOG_DOSYA)
                    yeni_log = pd.DataFrame([{
                        "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Kullanıcı": st.session_state.get("isim"),
                        "Aksiyon": row["İçerik"],
                        "Durum": "Aksiyon Bekleniyor",
                        "Onay":"",
                        "Yeni Tarih Talebi":"Onaylandı",
                        "Açıklama": onay_aciklama,
                        "Aşama":"Yeni Tarih Talebi İşlemleri"
                    }])
                    log_df = pd.concat([log_df, yeni_log], ignore_index=True)
                    log_df.to_excel(LOG_DOSYA, index=False)
                    
                    st.success("✅ Onaylandı ve kayıt güncellendi.")
                    st.rerun()
            with col2:
                if st.button("❌ Reddet", key=f"reddet_{i}"):
                    df.at[i, "Durum"] = row["Durum"]
                    df.at[i, "Onay"] = "Reddedildi"
                    df.at[i, "Yeni Tarih Talebi"] = "Reddedildi"
                    df.at[i, "Onaylayan"] = isim
                    df.at[i, "Onay Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df.at[i, "Onay Açıklaması"] = onay_aciklama
                    df.to_excel(TEV_AKSIYON, index=False)
                    
                    
                    
                    log_df = pd.read_excel(LOG_DOSYA)
                    yeni_log = pd.DataFrame([{
                        "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Kullanıcı": st.session_state.get("isim"),
                        "Aksiyon": row["İçerik"],
                        "Durum": row["Durum"],
                        "Onay":"Reddedildi",
                        "Yeni Tarih Talebi":"Reddedildi",
                        "Açıklama": onay_aciklama,
                        "Aşama":"Yeni Tarih Talebi İşlemleri"
                    }])
                    log_df = pd.concat([log_df, yeni_log], ignore_index=True)
                    log_df.to_excel(LOG_DOSYA, index=False)
                    
                    
                    st.warning("❌ Aksiyon reddedildi.")
                    st.rerun()
        st.markdown('<div style="height:2px;background:#ccc;margin:20px 0;"></div>', unsafe_allow_html=True)
    
    
    
    




st.markdown("""
             Aksiyonlar [Faaliyet, Sorumlu Kişi ve Dep, Termin Tarihi, Yapıldı/Yapılmadı, Kanıt, YeniTarih?]
            - Onay Aşaması
            - Onaylayan
            - Onay Tarihi
            - Onay Açıklaması
            
            Yeni tarih önerisinde de üst onayına gider.
            
            
            Strateji KPI 
            Banu Hn'a kadar onaya gider.
            Termin tarihi 3 ay, 6 ay, 12 ay
            hedef değer, gerçekleştirilen değer
            tamamlandı-tamamlanmadı
            açıklama yok
            kanıt belgesi olacak.
            
            erteleme,iptal,tamamlanmadı durumlarında Banu Hn'a kadar mail gider.
            üste onay, yapılmadı durumlarında gider.
            
            
            Görev atandı maili olacak, aksiyon kpi için.
            
            
            """)
            
