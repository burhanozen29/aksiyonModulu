# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:15:11 2025

@author: bozen
"""

# Sayfa 2: Aksiyon Güncelleme (taslak başlangıç)
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from aksiyon_kpi_modulu.config import KPI_DOSYA, KPI_SAYFA, TEV_AKSIYON, KANIT_KLASORU, LOG_DOSYA
from aksiyon_kpi_modulu.utils import aktif_ceyrek_bul
from aksiyon_kpi_modulu.database import tev_calisan

if not st.session_state.get("giris_yapildi", False):
    st.warning("🔒 Bu sayfaya erişmek için önce giriş yapmalısınız.")
    st.stop()
st.title("📊 Aksiyon Güncelleme Paneli")

moduller = ["Süreç Kararları","Toplantı Kararları","Diğer Kararlar","KPI"]
modul_sec = st.selectbox("Modül Seç", options=moduller, index=None, placeholder="Güncellenecek modülü seçin")

if modul_sec == "KPI":
    if not os.path.exists(KPI_DOSYA):
        st.error("KPI dosyası bulunamadı.")
        st.stop()

    df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)
    birim = st.session_state.birimler[0] if st.session_state.rol != "admin" else None
    if birim:
        df = df[df["Faaliyet Sahibi Birim"] == birim]

    aktif_ceyrek = "Hedef " + aktif_ceyrek_bul()
    ana_stratejiler = df[df[aktif_ceyrek].notna()]["Ana Strateji"].dropna().unique()
    ana_strateji = st.selectbox("1️⃣ Ana Strateji", options=sorted(ana_stratejiler), index=None)

    if ana_strateji:
        df_amac = df[df["Ana Strateji"] == ana_strateji]
        stratejik_amac = st.selectbox("2️⃣ Stratejik Amaç", options=sorted(df_amac["Stratejik Amaç"].dropna().unique()), index=None)
        if stratejik_amac:
            df_hedef = df_amac[df_amac["Stratejik Amaç"] == stratejik_amac]
            stratejik_hedef = st.selectbox("3️⃣ Stratejik Hedef", options=sorted(df_hedef["Stratejik Hedef"].dropna().unique()), index=None)
            if stratejik_hedef:
                df_faaliyet = df_hedef[df_hedef["Stratejik Hedef"] == stratejik_hedef]
                selected_kpi = st.selectbox("4️⃣ Faaliyet", options=sorted(df_faaliyet["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"].dropna().unique()), index=None)

                if selected_kpi:
                    kpi_row_idx = df[df["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"] == selected_kpi].index[0]
                    refDegerHedef = float(df.at[kpi_row_idx, aktif_ceyrek])
                    refDegerStr = df.at[kpi_row_idx, 'Hedef Ölçüsü']
                    refDeger = st.number_input("Gerçekleşen Değer", min_value=0.0, max_value=1.0 if refDegerStr == "Oran" else 100.0, step=0.01)

                    durum = "Tamamlandı" if refDeger >= refDegerHedef else st.selectbox("Durum", ["Tamamlanmadı", "Ertelendi", "İptal Edildi"])
                    aciklama = st.text_area("Açıklama / Gerekçe")
                    yeni_tarih = st.date_input("Yeni hedef tarih", value=datetime.today())

                    uploaded_file = st.file_uploader("📎 Kanıt Belgesi (ZORUNLU)", type=["pdf", "docx", "xlsx", "csv", "xls"])
                    if st.button("📩 Güncelle ve Kaydet"):
                        if not uploaded_file:
                            st.error("❗ Lütfen zorunlu dosyayı yükleyin!")
                        else:
                            os.makedirs(KANIT_KLASORU, exist_ok=True)
                            file_path = os.path.join(KANIT_KLASORU, uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.read())

                            df.at[kpi_row_idx, "Durum"] = durum
                            df.at[kpi_row_idx, "Açıklama"] = aciklama
                            df.at[kpi_row_idx, "Önerilen Yeni Tarih"] = yeni_tarih.strftime("%Y-%m-%d")
                            df.at[kpi_row_idx, "Güncelleme Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            df.at[kpi_row_idx, "Kanıt"] = uploaded_file.name
                            df.to_excel(KPI_DOSYA, sheet_name=KPI_SAYFA, index=False)
                            
                            
                            log_df = pd.read_excel(LOG_DOSYA)
                            yeni_log = pd.DataFrame([{
                                "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Kullanıcı": st.session_state.get("isim"),
                                "Aksiyon": selected_kpi,
                                "Durum": durum,
                                "Açıklama": aciklama,
                                "Yüklenen Dosya": uploaded_file.name,
                                "Aşama":"Aksiyon Güncelleme"
                            }])
                            log_df = pd.concat([log_df, yeni_log], ignore_index=True)
                            log_df.to_excel(LOG_DOSYA, index=False)

                            
                            

                            st.success("✅ Güncelleme kaydedildi.")
elif (modul_sec == "Toplantı Kararları") or (modul_sec == "Diğer Kararlar") or (modul_sec=="Süreç Kararları"):
    if st.session_state.rol == "admin":
        aksiyon_df = pd.read_excel(TEV_AKSIYON)
    else:
        aksiyon_df = pd.read_excel(TEV_AKSIYON)
        aksiyon_df = aksiyon_df[aksiyon_df["İşi Yapacak Birim"]==st.session_state.birimler[0]]
        aksiyon_df = aksiyon_df[~aksiyon_df["Onay"].str.contains("Onaylandı", na=False)]

        
    aksiyon_df = aksiyon_df[aksiyon_df["Modül"]==modul_sec]
    aksiyon_sec = aksiyon_df["İçerik"]
    aksiyon = st.selectbox("Aksiyon Seç", options=aksiyon_sec, index=None)
    if aksiyon:
        veriler = list(tev_calisan.find())
        kullanıcılar = pd.DataFrame(veriler)
        aksiyon_sorumlu_kisi = aksiyon_df.loc[aksiyon_df["İçerik"] == aksiyon, "Sorumlu Kişi"].values
        onaydurumu = aksiyon_df.loc[aksiyon_df["İçerik"]==aksiyon,"Onay"].values
        onay_durumu = st.selectbox("Onay Durumu", options=onaydurumu, disabled=True)
        sorumlu_kisi = st.selectbox("Sorumlu Kişi",
                                    options=aksiyon_sorumlu_kisi,
                                    disabled=True)
        
        if sorumlu_kisi:
            birim = kullanıcılar.loc[kullanıcılar["İsim"] == sorumlu_kisi,
                         "Birim"].values[0]
            sorumlu_birim = st.selectbox("Sorumlu Birim",
                                         options=birim,
                                         disabled=True)
            
            yeni_is_yapacak = st.radio("İşi Yapacak Yeni Kişiyi Seçmek İstiyor Musun?",
                                ["Evet","Hayır"],
                                horizontal=True,
                                index=1)
            aksiyon_is_yapacak = aksiyon_df.loc[aksiyon_df["İçerik"] == aksiyon, "İşi Yapacak Kişi"].values[0]
            if yeni_is_yapacak == "Hayır":
                isi_yapacak_kisi = st.selectbox("İşi Yapacak Kişiyi Seç",
                                                options=aksiyon_is_yapacak,
                                                disabled=True)
            elif yeni_is_yapacak == "Evet":
                aksiyon_is_yapacak_index = kullanıcılar[kullanıcılar["İsim"]==aksiyon_is_yapacak].index
                
                isi_yapacak_kisi = st.selectbox("İşi Yapacak Kişiyi Seç",
                                                options=kullanıcılar["İsim"],
                                                index=kullanıcılar.index.get_loc(aksiyon_is_yapacak_index[0]))
                
            if yeni_is_yapacak:
                birim2 = kullanıcılar.loc[kullanıcılar["İsim"] == isi_yapacak_kisi,
                         "Birim"].values[0]
                isi_yapacak_birim = st.selectbox("İşi Yapacak Birim",
                                                 options=birim2,
                                                 disabled=True)
                tamamlandi_mi = st.radio("Aksiyon tamamlandı mı?",
                                    ["Evet","Hayır"],
                                    horizontal=True,
                                    index=None)
                if tamamlandi_mi:
                    aciklama = st.text_area("Açıklama giriniz")
                    if aciklama:
                        if tamamlandi_mi == "Evet":
                            kanit_yukle = st.file_uploader("Tamamlandığına dair dosya yükle (ZORUNLU)",
                                                           type=["pdf", "docx", "xlsx","csv","xls"])
                            if kanit_yukle: 
                                if st.button("📩 Güncelle ve Kaydet"):
                                    index = aksiyon_df[aksiyon_df["İçerik"]==aksiyon].index
                                    
                                    if not index.empty:
                                        
                                        os.makedirs(KANIT_KLASORU, exist_ok=True)
                                        doc_name = kanit_yukle.name
                                        with open(os.path.join(KANIT_KLASORU, doc_name), "wb") as f:
                                            f.write(kanit_yukle.read())
                                        
                                        
                                        aksiyon_df = pd.read_excel(TEV_AKSIYON)
                                        
                                        aksiyon_df.loc[index, "Yapıldı Mı"] = tamamlandi_mi
                                        aksiyon_df.loc[index, "Güncelleme Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        aksiyon_df.loc[index, "Kanıt"] = kanit_yukle.name  # veya başka bir kullanıcı girdisi
                                        aksiyon_df.loc[index, "Açıklama"] = aciklama
                                        aksiyon_df.loc[index, "İşi Yapacak Kişi"] = isi_yapacak_kisi
                                        aksiyon_df.loc[index, "İşi Yapacak Birim"] = isi_yapacak_birim
                                        aksiyon_df.loc[index, "Durum"] = "Tamamlandı"
                                        aksiyon_df.loc[index, "Onay"] = "Onay Bekliyor"
                                        # Excel'e yaz
                                        aksiyon_df.to_excel(TEV_AKSIYON, index=False)
                                        
                                        
                                        log_df = pd.read_excel(LOG_DOSYA)
                                        yeni_log = pd.DataFrame([{
                                            "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "Kullanıcı": st.session_state.get("isim"),
                                            "Aksiyon": aksiyon,
                                            "Durum": "Tamamlandı",
                                            "Onay":"Onay Bekliyor",
                                            "Açıklama": aciklama,
                                            "Yüklenen Dosya": kanit_yukle.name,
                                            "Aşama":"Aksiyon Güncelleme"
                                        }])
                                        log_df = pd.concat([log_df, yeni_log], ignore_index=True)
                                        log_df.to_excel(LOG_DOSYA, index=False)
                                        
                                        st.write("Kaydedildi")
                                    else:
                                        st.write("Güncellenecek satır bulunamadı")
                        else: 
                            yeni_tarih_sec = st.radio("Yeni Tarih Girmek İstiyor Musun?",
                                                ["Evet","Hayır"],
                                                horizontal=True,
                                                index=1)
                            if yeni_tarih_sec == "Evet":
                                yeni_tarih = st.date_input("Yeni hedef tarih", value=datetime.today())
                            else:
                                yeni_tarih = ""
                            
                            # df.at[kpi_row_idx, "Önerilen Yeni Tarih"] = yeni_tarih.strftime("%Y-%m-%d")
                            
                            if st.button("📩 Güncelle ve Kaydet"):
                                index = aksiyon_df[aksiyon_df["İçerik"]==aksiyon].index
                                
                                if not index.empty:
                                    aksiyon_df = pd.read_excel(TEV_AKSIYON)
                                    
                                    aksiyon_df.loc[index, "Yapıldı Mı"] = tamamlandi_mi
                                    aksiyon_df.loc[index, "Güncelleme Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    aksiyon_df.loc[index, "Kanıt"] = ""  # veya başka bir kullanıcı girdisi
                                    aksiyon_df.loc[index, "Açıklama"] = aciklama
                                    aksiyon_df.loc[index, "İşi Yapacak Kişi"] = isi_yapacak_kisi
                                    aksiyon_df.loc[index, "İşi Yapacak Birim"] = isi_yapacak_birim
                                    aksiyon_df.loc[index, "Yeni Tarih"] = yeni_tarih
                                    aksiyon_df.loc[index, "Durum"] = "Tamamlanmadı"
                                    aksiyon_df.loc[index, "Onay"] = "Onay Bekliyor"
                                    if yeni_tarih != "":
                                        aksiyon_df.loc[index, "Yeni Tarih Talebi"] = "Onay Bekliyor"
                                    # Excel'e yaz
                                    aksiyon_df.to_excel(TEV_AKSIYON, index=False)
                                    
                                    log_df = pd.read_excel(LOG_DOSYA)
                                    if yeni_tarih == "":
                                        yeni_log = pd.DataFrame([{
                                            "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "Kullanıcı": st.session_state.get("isim"),
                                            "Aksiyon": aksiyon,
                                            "Durum": "Tamamlanmadı",
                                            "Onay":"Onay Bekliyor",
                                            "Açıklama": aciklama,
                                            "Aşama":"Aksiyon Güncelleme"
                                        }])
                                    else:
                                        yeni_log = pd.DataFrame([{
                                            "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "Kullanıcı": st.session_state.get("isim"),
                                            "Aksiyon": aksiyon,
                                            "Durum": "Tamamlanmadı",
                                            "Onay":"Onay Bekliyor",
                                            "Yeni Tarih Talebi":"Onay Bekliyor",
                                            "Açıklama": aciklama,
                                            "Yeni Tarih":yeni_tarih,
                                            "Aşama":"Yeni Tarih Önerisi"
                                        }])
                                    log_df = pd.concat([log_df, yeni_log], ignore_index=True)
                                    log_df.to_excel(LOG_DOSYA, index=False)
                                    
                                    
                                    st.write("Kaydedildi")
                                else:
                                    st.write("Güncellenecek satır bulunamadı")
                            
                    
    st.stop()
        # SORUMLU KİŞİ ALTINDAKİ KİŞİYE ATAYABİLİR
        # YAPILDI İSE BELGE YÜKLE
        # AÇIKLAMA ALANI
        # YAPILMADI İSE YENİ TARİH ÖNER. BİR ÜST BİRİME GİDER.
