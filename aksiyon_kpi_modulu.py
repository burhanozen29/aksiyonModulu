import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO
import plotly.express as px
import time

# === Dosya yolları ===
KPI_DOSYA = "TEV_2024_KPI.xlsx"
KPI_SAYFA = "SP TEV"
KULLANICI_DOSYA = "kullanicilar.xlsx"
LOG_DOSYA = "log_kpi_guncelleme.xlsx"
KANIT_KLASORU = "kanitlar"
TEV_CALISAN = "TEV_çalışan_listesi.xlsx"
TEV_AKSIYON = "Aksiyonlar.xlsx"

def aktif_ceyrek_bul():
    ay = datetime.today().month
    yil = datetime.today().year

    if yil == 2025:
        if ay in [1, 2, 3]:
            return "2025 Q1"
        elif ay in [4, 5, 6]:
            return "2025 Q2"
        elif ay in [7, 8, 9]:
            return "2025 Q3"
        elif ay in [10, 11, 12]:
            return "2025 Q4"
    elif yil == 2026:
        if ay in [1, 2, 3]:
            return "2026 Q1"
        elif ay in [4, 5, 6]:
            return "2026 Q2"
        elif ay in [7,8,9]:
            return "2026 Q3"
        elif ay in [10,11,12]:
            return "2026 Q4"
    elif yil == 2027:
        if ay in [1, 2, 3]:
            return "2027 Q1"
        elif ay in [4, 5, 6]:
            return "2027 Q2"
        elif ay in [7,8,9]:
            return "2027 Q3"
        elif ay in [10,11,12]:
            return "2027 Q4"
    return None

# === Kullanıcı doğrulama ===
def kullanici_dogrula(kullanici_adi, sifre):
    if not os.path.exists(KULLANICI_DOSYA):
        return None
    df_users = pd.read_excel(KULLANICI_DOSYA)
    row = df_users[(df_users["Kullanıcı Adı"] == kullanici_adi) & (df_users["Şifre"] == sifre)]
    if not row.empty:
        birimler = row.iloc[0]["Birimler"].split(",")
        rol = row.iloc[0]["Rol"]
        return {"birimler": [b.strip() for b in birimler], "rol": rol}
    return None

# === Oturum yönetimi ===
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False

# === Giriş ekranı ===
if not st.session_state.giris_yapildi:
    def giris_yap(otomatik=False):
        sonuc = kullanici_dogrula(st.session_state.kullanici_input, st.session_state.sifre)
        if sonuc:
            st.session_state.giris_yapildi = True
            st.session_state.kullanici = st.session_state.kullanici_input
            st.session_state.birimler = sonuc["birimler"]
            st.session_state.rol = sonuc["rol"]
            if not otomatik:
                st.rerun()
        else:
            st.session_state.hata_mesaji = "❌ Kullanıcı adı veya şifre hatalı."

    st.title("🔐 KPI Takip Sistemi - Giriş")
    st.text_input("Kullanıcı Adı", key="kullanici_input")
    st.text_input("Şifre", type="password", key="sifre", on_change=giris_yap, kwargs={"otomatik": True})

    if st.button("Giriş Yap"):
        giris_yap(otomatik=False)

    if "hata_mesaji" in st.session_state:
        st.error(st.session_state.hata_mesaji)

    st.stop()

# === Menü ===
st.sidebar.title("📁 Menü")
sekmeler = ["Aksiyon Ekle","Aksiyon Güncelle","Aksiyon Raporlama", "Aksiyon Takvim Görünümü"]
if st.session_state.rol == "admin":
    sekmeler.extend(["Güncelleme Geçmişi", "Kullanıcı Yönetimi"])
secili = st.sidebar.radio("Lütfen işlem seçin:", sekmeler)

# === KPI dosyasını oku ===
if not os.path.exists(KPI_DOSYA):
    st.error("KPI dosyası bulunamadı.")
    st.stop()

df = pd.read_excel(KPI_DOSYA, sheet_name=KPI_SAYFA)

# == Aksiyon Ekleme ==
if secili == "Aksiyon Ekle":
    st.title("Aksiyon Ekleme Paneli")
    def reset_modul():
        aksiyon_data = pd.DataFrame({
                    "Modül": [modul_ekle],
                    "İçerik": [modul_icerik],
                    "Sorumlu Birim" : [sorumlu_birim_sec],
                    "Sorumlu Kişi" : [sorumlu_kisi_sec],
                    "İşi Yapacak Birim" : [isi_yapacak_birim_sec],
                    "İşi Yapacak Kişi" : [isi_yapacak_kisi_sec],
                    "Ölçü Birimi" : [olcu_ekle],
                    "Referans Değeri":[refDeger],
                    "MinMax":[minMax],
                    "Termin Tarihi":[terminTarihi],
                    "Aksiyon Ekleme Tarihi":datetime.now()
                })
        
        if os.path.exists(TEV_AKSIYON):
            # Mevcut Excel'den verileri oku
            mevcut_df = pd.read_excel(TEV_AKSIYON)
            # Yeni veriyi ekle
            guncel_df = pd.concat([mevcut_df, aksiyon_data], ignore_index=True)
        else:
            # İlk kez oluşturuluyor
            guncel_df = aksiyon_data
        
        
        
        # Dosyayı kaydet
        guncel_df.to_excel(TEV_AKSIYON, index=False)
        st.success("Veri başarıyla eklendi!")
        time.sleep(2)
        st.session_state["modul"] = None
        st.session_state["içerik"] = None
        st.session_state["sorumluBirim"] = None
        st.session_state["sorumluKişi"] = None
        st.session_state["işiYapacakBirim"] = None
        st.session_state["işiYapacakKişi"] = None
        st.session_state["ölçüTipi"] = None
        st.session_state["minMax"] = None
        st.session_state["referans"] = 0.0
        st.session_state["termin_tarihi"] = None
        

    moduller = ["Süreç Kararları","Toplantı Kararları","Diğer Kararlar"]
    modul_ekle = st.selectbox("Modül Seç",options=moduller, index=None, key="modul")
    if modul_ekle:
        modul_icerik = st.text_area(f"{modul_ekle} içeriğini girin", key="içerik")
        if modul_icerik:
            kullanıcılar = pd.read_excel(TEV_CALISAN)
            sorumlu_kullanıcılar = kullanıcılar[kullanıcılar["Bağlı Kişi Birim"] != "Genel Müdürlük"]
            sorumlu_kullanıcılar = sorumlu_kullanıcılar[sorumlu_kullanıcılar["Bağlı Kişi Birim"] != "-"]
            sorumlu_birim = sorumlu_kullanıcılar.groupby("Birim")
            sorumlu_birim_sec = st.selectbox("Sorumlu Birim Seç",
                                             options=sorumlu_birim,
                                             index=None,
                                             key="sorumluBirim")
            if sorumlu_birim_sec:
                sorumlu_kisi = sorumlu_kullanıcılar[sorumlu_kullanıcılar["Birim"] == sorumlu_birim_sec]["İsim"]
                sorumlu_kisi_sec = st.selectbox("Sorumlu Kişi Seç",
                                                options=sorumlu_kisi,
                                                index=None,
                                                key="sorumluKişi")
                if sorumlu_kisi_sec:
                    
                    isi_yapacak_birim = kullanıcılar.groupby("Birim")
                    isi_yapacak_birim_sec = st.selectbox("İşi Yapacak Birim Seç",
                                                     options = isi_yapacak_birim,
                                                     index=None,
                                                     key="işiYapacakBirim")
                    
                    if isi_yapacak_birim_sec:
                        isi_yapacak_kisi = kullanıcılar[kullanıcılar["Birim"] == isi_yapacak_birim_sec]["İsim"]
                        isi_yapacak_kisi_sec = st.selectbox("İşi Yapacak Kişi Seç",
                                                            options=isi_yapacak_kisi,
                                                            index=None,
                                                            key="işiYapacakKişi")
                        if isi_yapacak_kisi_sec:
                            olcu_birimi = ["Oran","Sayı"]
                            olcu_ekle = st.selectbox("Ölçü Birimi Ekle",
                                                     options=olcu_birimi,
                                                     index=None,
                                                     key="ölçüTipi")
                            if olcu_ekle:
                                minMax = st.radio("Referans Değeri Sınırı",
                                                  ["En Az","En Çok"],
                                                  horizontal = True,
                                                  index=None,
                                                  key="minMax")
                                if minMax:
                                    if olcu_ekle == "Oran":
                                        refDeger = st.number_input(f"{olcu_ekle} referans değerini girin (0-100)(%)",
                                                               min_value=0.0,
                                                               max_value=100.0,
                                                               step=0.1,
                                                               key="referans")
                                        refDeger = refDeger/100
                                    else:
                                        refDeger = st.number_input(f"{olcu_ekle} referans değerini girin",
                                                               min_value=0,
                                                               max_value=1000,
                                                               step=1,
                                                               key="referans")
                                    terminTarihi = st.date_input("Termin Tarihi Girin",
                                                                 value=datetime.today(),
                                                                 min_value=datetime.today(),
                                                                 key="termin_tarihi")
                                    if terminTarihi:
                                        st.button("Aksiyon Ekle", on_click=reset_modul)
    st.stop()



# === KPI Takvim Görünümü ===
if secili == "Aksiyon Takvim Görünümü":
    st.title("🗓️ KPI Takvim / Timeline Görünümü")

    # Birim seçimi
    birim_secimi = st.multiselect(
        "📌 Birim",
        options=sorted(df["Faaliyet Sahibi Birim"].dropna().unique()),
        default=None,
        placeholder="Birim(leri) Seçin (Seçim yapmazsanız tümü gösterilir)"
    )

    # Güncelleme tarihi dolu olanları filtrele
    df_timeline = df[pd.notnull(df["Güncelleme Tarihi"])].copy()

    # Eğer birim seçilmişse filtrele
    if birim_secimi:
        df_timeline = df_timeline[df_timeline["Faaliyet Sahibi Birim"].isin(birim_secimi)]

    if df_timeline.empty:
        st.warning("Gösterilecek zaman çizelgesi bulunamadı.")
    else:
        fig = px.timeline(
            df_timeline,
            x_start="Güncelleme Tarihi",
            x_end="İlgili Faaliyet Başlangıç Tarihi",
            y="Stratejik Hedef",
            color="Durum",
            title="KPI Süreç Takvimi"
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    st.stop()
#%%
# # === KPI Ekleme ve Silme ===
# elif secili == "KPI Ekleme/Silme":
#     st.title("KPI Ekle veya Sil")
#     st.caption("⭐ Yeni bir KPI eklemek ya da varolan bir KPI'yı silmek/güncellemek için bu ekran kullanılır.")
    
#     st.subheader("➕ KPI Ekle")
    
#     st.divider()
    
#     mevcut_birimler = sorted(df["Faaliyet Sahibi Birim"].dropna().unique())
#     secim_tipi = st.radio(
#         "1️⃣ İlgili KPI'yı nasıl eklemek istersiniz?",
#         ["İlgili Birim Seç", "İlgili KPI Yok"],
#         horizontal=True
#     )
#     ilgiliKPI = None
#     kpi188 = None
#     anaStrateji = None
#     stratejikAmac = None
#     stratejikAmacSahibi = None
#     stratejikHedef = None
#     hedefeUlasmakFaaliyet = None
#     faaliyetSahibi = None 
#     faaliyetDestek = None
#     faaliyetBaslangic = None 
#     faaliyetBitis = None 
#     hedefOlcusu = None 
#     ilgiliKPI1 = None 
#     hedef2025q1 = None
#     hedef2025q2 = None
#     hedef2025q3 = None
#     hedef2025q4 = None
#     hedef2026q1 = None
#     hedef2026q2 = None
#     hedef2026q3 = None
#     hedef2026q4 = None
#     hedef2027q1 = None
#     hedef2027q2 = None
#     hedef2027q3 = None
#     hedef2027q4 = None
#     butce = None
    
    
#     if "yeniKPI" not in st.session_state:
#         st.session_state["yeniKPI"] = pd.DataFrame(columns=["İlgili KPI",
#                                                             "188 KPI",
#                                                             "Ana Strateji",
#                                                             "Stratejik Amaç",
#                                                             "Stratejik Amaç Sahibi",
#                                                             "Stratejik Hedef",
#                                                             "Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyet",
#                                                             "Faaliyet Sahibi",
#                                                             "Faaliyet Destek",
#                                                             "Faaliyet Başlangıcı",
#                                                             "Faaliyet Bitişi",
#                                                             "Hedef Ölçüsü",
#                                                             "İlgili KPI.1",
#                                                             "2025q1",
#                                                             "2025q2",
#                                                             "2025q3",
#                                                             "2025q4",
#                                                             "2026q1",
#                                                             "2026q2",
#                                                             "2026q3",
#                                                             "2026q4",
#                                                             "2027q1",
#                                                             "2027q2",
#                                                             "2027q3",
#                                                             "2027q4",
#                                                             "Bütçe Gerekli Mi?"])
     
    
#     if secim_tipi == "İlgili Birim Seç": ilgiliKPI = st.multiselect("İlgili KPI", options=mevcut_birimler, placeholder="İlgili KPI")
#     else: ilgiliKPI = "x"
#     st.divider()
    
#     if ilgiliKPI:
#         st.session_state[ilgiliKPI] = "ilgiliKPIkey"
#         kpi188 = st.text_input("2️⃣ 188 KPI metnini girin")
#         st.divider()
    
#     if kpi188:
#         mevcut_anaStrateji = sorted(df["Ana Strateji"].dropna().unique())
#         secim_tipi = st.radio(
#             "3️⃣ Ana stratejiyi nasıl eklemek istersiniz?",
#             ["Mevcut ana stratejiden seç","Yeni Ekle"],
#             horizontal=True
#             )
#         if secim_tipi == "Mevcut ana stratejiden seç": anaStrateji=st.multiselect("Ana Strateji",options=mevcut_anaStrateji,placeholder="Ana Strateji Seç")
#         else: 
#             ilk_haneler = [int(str(s)[0]) for s in mevcut_anaStrateji if str(s)[0].isdigit()]
#             en_buyuk_ilk_hane = max(ilk_haneler)
#             anaStrateji = st.text_input(f"Ana Stratejini Girin (Strateji numarası girmeyi unutmayın, en son numara: {en_buyuk_ilk_hane}.)")
#         st.divider()
        
#     if anaStrateji:
#         secim_tipi = st.radio(
#             "4️⃣ Stratejik amacı nasıl eklemek istersiniz?",
#             ["Mevcut stratejik amaçtan seç","Yeni Ekle"],
#             horizontal=True
#             )
        
#         mevcut_stratejikAmac = sorted(df["Stratejik Amaç"].dropna().unique())
#         ilk_hane_degeri = anaStrateji[0][:2]
#         if secim_tipi == "Mevcut stratejik amaçtan seç":
#             stratejikAmac = [amac for amac in mevcut_stratejikAmac if amac.startswith(ilk_hane_degeri)]
#             stratejikAmac = st.selectbox("Stratejik Amaç",
#                                          options=stratejikAmac,placeholder="Stratejik Amaç Seç",
#                                          index=None
#                                          )
#         else:
#             stratejikAmac = st.text_input(f"Stratejik Amacı Girin {ilk_hane_degeri} ile başlamalı.")
#         st.divider()
    
#     if stratejikAmac:
#         mevcut_stratejikAmacSahibi = sorted(df["Stratejik Amaç Sahibi"].dropna().unique())
#         stratejikAmacSahibi = st.selectbox("5️⃣ Stratejik Amaç Sahibi",
#                                      options=mevcut_stratejikAmacSahibi,placeholder="Stratejik Amaç Seç",
#                                      index=None
#                                      )
#         st.divider()
    
#     if stratejikAmacSahibi:
#         secim_tipi = st.radio(
#             "6️⃣ Stratejik hedefi nasıl eklemek istersiniz?",
#             ["Mevcut stratejik hedeften seç","Yeni Ekle"],
#             horizontal=True
#             )
        
#         mevcut_stratejikHedef = sorted(df["Stratejik Hedef"].dropna().unique())
#         ilk_hane_degeri = stratejikAmac[:4]
#         if secim_tipi == "Mevcut stratejik hedeften seç":
#             stratejikHedef = [amac for amac in mevcut_stratejikHedef if amac.startswith(ilk_hane_degeri)]
#             stratejikHedef = st.selectbox("Stratejik Amaç",
#                                          options=stratejikHedef,placeholder="Stratejik Amaç Seç",
#                                          index=None
#                                          )
#         else:
#             stratejikHedef = st.text_input(f"Stratejik Hedefi Girin {ilk_hane_degeri} ile başlamalı.")
#         st.divider()

#     if stratejikHedef:
#         secim_tipi = st.radio(
#             "7️⃣ Hedefe ulaşmak için gerçekleştirilecek faaliyeti nasıl eklemek istersiniz?",
#             ["Mevcut faaliyetten seç","Yeni Ekle"],
#             horizontal=True
#             )
        
#         mevcut_faaliyet = sorted(df["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"].dropna().unique())
#         ilk_hane_degeri = stratejikHedef[:6]
#         if secim_tipi == "Mevcut faaliyetten seç":
#             hedefeUlasmakFaaliyet = [amac for amac in mevcut_faaliyet if amac.startswith(ilk_hane_degeri)]
#             hedefeUlasmakFaaliyet = st.selectbox("Stratejik Amaç",
#                                          options=hedefeUlasmakFaaliyet,placeholder="Faaliyet Seç",
#                                          index=None
#                                          )
#         else:
#             hedefeUlasmakFaaliyet = st.text_input(f"Faaliyet Girin {ilk_hane_degeri} ile başlamalı.")
#         st.divider()
    
#     if hedefeUlasmakFaaliyet:
#         mevcut_faaliyetSahibi = sorted(df["Faaliyet Sahibi Birim"].dropna().unique())
#         faaliyetSahibi = st.selectbox("8️⃣ Faaliyet Sahibi Birim",
#                                      options=mevcut_faaliyetSahibi,placeholder="Faaliyet Sahibi Seç",
#                                      index=None
#                                      )
#         st.divider()
    
#     if faaliyetSahibi:
#         mevcut_faaliyetDestek = sorted(df["Faaliyet Destek Birim"].dropna().unique())
#         faaliyetDestek = st.selectbox("9️⃣ Faaliyet Destek Birim",
#                                      options=mevcut_faaliyetDestek,placeholder="Faaliyet Destek Seç",
#                                      index=None
#                                      )
#         st.divider()
    
#     if faaliyetDestek:
#         faaliyetBaslangic = st.date_input("1️⃣0️⃣ Faaliyet başlangıç tarihi",
#                                           value=datetime.today(),
#                                           key="faaliyetBaslangic")
#         st.divider()
        
#     if faaliyetBaslangic:
#         faaliyetBitis = st.date_input("1️⃣1️⃣ Faaliyet bitiş tarihi",
#                                       value=faaliyetBaslangic,
#                                       min_value=faaliyetBaslangic,
#                                       key="faaliyetBitis")
#         st.divider()
    
#     if faaliyetBitis:
#         mevcut_hedefOlcusu = sorted(df['Hedef Ölçüsü'].dropna().unique())
#         hedefOlcusu = st.selectbox("1️⃣2️⃣ Hedef Ölçüsü",
#                                    options=mevcut_hedefOlcusu,
#                                    placeholder="Hedef Ölçüsü Seçin",
#                                    index=None)
#         st.divider()
    
#     if hedefOlcusu:
#         mevcut_ilgiliKPI1 = sorted(df['İlgili KPI.1'].dropna().unique())
        
#         secim_tipi = st.radio(
#             "1️⃣3️⃣ İlgili KPI.1'i nasıl eklemek istersiniz?",
#             ["Mevcut İlgili KPI.1'den seç","Yeni Ekle"],
#             horizontal=True
#             )
        
#         if secim_tipi == "Mevcut İlgili KPI.1'den seç":
#             ilgiliKPI1 = st.selectbox("İlgili KPI.1",
#                                          options=mevcut_ilgiliKPI1,placeholder="İlgili KPI.1 Seç",
#                                          index=None
#                                          )
#         else:
#             ilgiliKPI1 = st.text_input("İlgili KPI.1 girin")
#         st.divider()
    
#     if ilgiliKPI1:
#         hedef2025q1 = st.number_input("2025'in ilk çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2025q2 = st.number_input("2025'in ikinci çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2025q3 = st.number_input("2025'in üçüncü çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2025q4 = st.number_input("2025'in son çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2026q1 = st.number_input("2026'nın ilk çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2026q2 = st.number_input("2026'nın ikinci çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2026q3 = st.number_input("2026'nın üçüncü çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2026q4 = st.number_input("2026'nın son çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2027q1 = st.number_input("2027'nin ilk çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2027q2 = st.number_input("2027'nin ikinci çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2027q3 = st.number_input("2027'nin üçüncü çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
#         hedef2027q4 = st.number_input("2027'nin son çeyreği için hedef girin",
#                                       min_value=0.0,
#                                       step=1.0)
        
        
#         if hedef2025q1 == 0:
#             hedef2025q1 = None
#         elif float(f"0.{str(hedef2025q1).split('.')[-1]}") == 0:
#                  hedef2025q1 = int(hedef2025q1)
    
#         if hedef2025q2 == 0:
#             hedef2025q2 = None
#         elif float(f"0.{str(hedef2025q2).split('.')[-1]}") == 0:
#                  hedef2025q2 = int(hedef2025q2)
    
#         if hedef2025q3 == 0:
#             hedef2025q3 = None
#         elif float(f"0.{str(hedef2025q3).split('.')[-1]}") == 0:
#                  hedef2025q3 = int(hedef2025q3)
    
#         if hedef2025q4 == 0:
#             hedef2025q4 = None
#         elif float(f"0.{str(hedef2025q4).split('.')[-1]}") == 0:
#                  hedef2025q4 = int(hedef2025q4)
        
#         if hedef2026q1 == 0:
#             hedef2026q1 = None
#         elif float(f"0.{str(hedef2026q1).split('.')[-1]}") == 0:
#                  hedef2026q1 = int(hedef2026q1)
    
#         if hedef2026q2 == 0:
#             hedef2026q2 = None
#         elif float(f"0.{str(hedef2026q2).split('.')[-1]}") == 0:
#                  hedef2026q2 = int(hedef2026q2)
    
#         if hedef2026q3 == 0:
#             hedef2026q3 = None
#         elif float(f"0.{str(hedef2026q3).split('.')[-1]}") == 0:
#                  hedef2026q3 = int(hedef2026q3)
    
#         if hedef2026q4 == 0:
#             hedef2026q4 = None
#         elif float(f"0.{str(hedef2026q4).split('.')[-1]}") == 0:
#                  hedef2026q4 = int(hedef2026q4)
        
#         if hedef2027q1 == 0:
#             hedef2027q1 = None
#         elif float(f"0.{str(hedef2027q1).split('.')[-1]}") == 0:
#                  hedef2027q1 = int(hedef2027q1)
    
#         if hedef2027q2 == 0:
#             hedef2027q2 = None
#         elif float(f"0.{str(hedef2027q2).split('.')[-1]}") == 0:
#                  hedef2027q2 = int(hedef2027q2)
    
#         if hedef2027q3 == 0:
#             hedef2027q3 = None
#         elif float(f"0.{str(hedef2027q3).split('.')[-1]}") == 0:
#                  hedef2027q3 = int(hedef2027q3)
    
#         if hedef2027q4 == 0:
#             hedef2027q4 = None
#         elif float(f"0.{str(hedef2027q4).split('.')[-1]}") == 0:
#                  hedef2027q4 = int(hedef2027q4)
        
#         butceSec = st.radio(
#             "Bütçe Gerekli Mi",
#             ["Evet","Hayır"],
#             horizontal= True,
#             index=None,
#             key = 'butceKey'
#             )
#         if butceSec == "Evet": butce = "E"
#         elif butceSec == "Hayır": butce = "H"
        
#     if butce:
#         yeniKPI = {"İlgili KPI": ilgiliKPI,
#                    "188 KPI": kpi188,
#                    "Ana Strateji": anaStrateji[0],
#                    "Stratejik Amaç": stratejikAmac,
#                    "Stratejik Amaç Sahibi":stratejikAmacSahibi,
#                    "Stratejik Hedef":stratejikHedef,
#                    "Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyet":hedefeUlasmakFaaliyet,
#                    "Faaliyet Sahibi":faaliyetSahibi,
#                    "Faaliyet Destek":faaliyetDestek,
#                    "Faaliyet Başlangıcı":faaliyetBaslangic,
#                    "Faaliyet Bitişi":faaliyetBitis,
#                    "Hedef Ölçüsü":hedefOlcusu,
#                    "İlgili KPI.1":ilgiliKPI1,
#                    "2025q1":hedef2025q1,
#                    "2025q2":hedef2025q2,
#                    "2025q3":hedef2025q3,
#                    "2025q4":hedef2025q4,
#                    "2026q1":hedef2026q1,
#                    "2026q2":hedef2026q2,
#                    "2026q3":hedef2026q3,
#                    "2026q4":hedef2026q4,
#                    "2027q1":hedef2027q1,
#                    "2027q2":hedef2027q2,
#                    "2027q3":hedef2027q3,
#                    "2027q4":hedef2027q4,
#                    "Bütçe Gerekli Mi?":butce
#                    }
        
#         st.session_state["yeniKPI"] =  pd.DataFrame([yeniKPI])
        
#         st.divider() 
        
#         st.dataframe(st.session_state["yeniKPI"],
#                      use_container_width=True,
#                      hide_index=True)
        
#         st.divider()
        
#         def sayfaYonlendir():
#             st.warning("KPI eklendi")
#             time.sleep(1)
#             st.session_state["sessionSayfa"] = "KPI Ekleme/Silme"
#             kpi_input_keys= ["butceKey","ilgiliKPIkey"]
#             for key in kpi_input_keys:
#                 if key in st.session_state:
#                     del st.session_state[key]
            
            
            
#         if st.button("Yeni KPI'ı ekle", on_click=sayfaYonlendir):
#             st.write("kpisilmebutonu")
        
#     st.stop()
#%%

# === Güncelleme Geçmişi ===
elif secili == "Güncelleme Geçmişi":
    st.title("🕓 KPI Güncelleme Geçmişi")
    if os.path.exists(LOG_DOSYA):
        log_df = pd.read_excel(LOG_DOSYA)
        st.dataframe(log_df.sort_index(ascending=False))
        with st.expander("⬇️ Excel olarak indir"):
            excel_buffer = BytesIO()
            log_df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            st.download_button("📥 İndir", data=excel_buffer, file_name="log_kpi_guncelleme.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Henüz hiç log kaydı bulunmamaktadır.")
    st.stop()

# === Kullanıcı Yönetimi ===
elif secili == "Kullanıcı Yönetimi":
    st.title("👤 Yeni Kullanıcı Ekle veya Güncelle")

    # Mevcut birimleri oku
    mevcut_birimler = sorted(df["Faaliyet Sahibi Birim"].dropna().unique())

    yeni_kullanici = st.text_input("Kullanıcı Adı")
    yeni_sifre = st.text_input("Şifre", type="password")
    secilen_birimler = st.multiselect("Birim(ler)", options=mevcut_birimler, placeholder="Birim(ler) Seçin")
    yeni_rol = st.selectbox("Rol", ["admin", "kullanıcı"], index=None, placeholder="Rol Seçin")

    if os.path.exists(KULLANICI_DOSYA):
        df_users = pd.read_excel(KULLANICI_DOSYA)
    else:
        df_users = pd.DataFrame(columns=["Kullanıcı Adı", "Şifre", "Birimler", "Rol"])

    mevcut_kullanicilar = sorted(df_users["Kullanıcı Adı"].dropna().unique())

    if st.button("➕ Ekle / Güncelle"):
        if not (yeni_kullanici and yeni_sifre and secilen_birimler and yeni_rol):
            st.warning("Tüm alanları doldurmalısınız.", icon="🚨")
        else:
            yeni_kayit = {
                "Kullanıcı Adı": yeni_kullanici,
                "Şifre": yeni_sifre,
                "Birimler": ",".join(secilen_birimler),
                "Rol": yeni_rol
            }

            if yeni_kullanici in df_users["Kullanıcı Adı"].values:
                df_users.loc[df_users["Kullanıcı Adı"] == yeni_kullanici, ["Şifre", "Birimler", "Rol"]] = \
                    yeni_sifre, ",".join(secilen_birimler), yeni_rol
                st.success("✅ Kullanıcı bilgileri güncellendi.")
            else:
                df_users = pd.concat([df_users, pd.DataFrame([yeni_kayit])], ignore_index=True)
                st.success("✅ Yeni kullanıcı eklendi.")

            df_users.to_excel(KULLANICI_DOSYA, index=False)
            time.sleep(1)
            st.rerun()

    
    st.divider()
    # Kullanıcı Sil
    st.title("❌ Kullanıcı Sil")
    
    # Session state ile onay süreci kontrolü
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = None
    
    mevcut_kullanici = st.selectbox(
        "Silinecek Kullanıcı", 
        options=mevcut_kullanicilar,
        index=None,
        placeholder="Kullanıcı Seçin"
    )
    
    if st.button("➖ Sil"):
        if not mevcut_kullanici:
            st.warning("Mevcut kullanıcı seçmelisiniz.", icon="🚨")
        else:
            st.session_state.selected_user = mevcut_kullanici
            st.session_state.confirm_delete = True
    
    # Eğer silme onayı bekleniyorsa
    if st.session_state.confirm_delete:
        st.warning(f"🛑 '{st.session_state.selected_user}' kullanıcısını silmek istediğinize emin misiniz?")
    
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Evet, Sil"):
                if os.path.exists(KULLANICI_DOSYA):
                    if st.session_state.selected_user in df_users["Kullanıcı Adı"].values:
                        df_users = df_users[df_users["Kullanıcı Adı"] != st.session_state.selected_user]
                        df_users.to_excel(KULLANICI_DOSYA, index=False)
                        st.success("🚫 Kullanıcı silindi.")
                        time.sleep(1)
                        st.session_state.confirm_delete = False
                        st.session_state.selected_user = None
                        st.rerun()
    
        with col2:
            if st.button("❌ Hayır, Vazgeç"):
                st.session_state.confirm_delete = False
                st.session_state.selected_user = None
                st.info("Silme işlemi iptal edildi.")
                time.sleep(1)
                st.rerun()
   
    st.divider()
    
    show_password = st.checkbox("Şifreyi Göster")
    if show_password:
        st.dataframe(df_users)
    else:
        df_masked = df_users.copy()
        df_masked["Şifre"] = df_masked["Şifre"].apply(lambda x: "*" * len(x))
        st.dataframe(df_masked)
        
    if os.path.exists(TEV_CALISAN):
        df_tev = pd.read_excel(TEV_CALISAN)
    else:
        df_tev = pd.DataFrame()
    st.dataframe(df_tev)
    
    
    st.stop()

# === KPI Raporlama ===
elif secili == "Aksiyon Raporlama":
    st.title("📈 KPI Raporlama ve Filtreleme")

    # Yalnızca kullanıcıya tanımlı birimleri göster
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

# === KPI Güncelleme ===
if st.session_state.rol == "admin":
    df_filtered = df.copy()
else:
    df_filtered = df[df["Faaliyet Sahibi Birim"].isin(st.session_state.birimler)]

if df_filtered.empty:
    st.warning("Bu kullanıcıya atanmış KPI bulunamadı.")
    st.stop()

if "last_selected_kpi" not in st.session_state:
    st.session_state.last_selected_kpi = None
if "durum" not in st.session_state:
    st.session_state.durum = "Tamamlandı"
if "aciklama" not in st.session_state:
    st.session_state.aciklama = ""
if "yeni_tarih" not in st.session_state:
    st.session_state.yeni_tarih = None


aktif_ceyrek = aktif_ceyrek_bul()

st.title(f"📊 Aksiyon Güncelleme Paneli ({aktif_ceyrek})")

# Hiyerarşik filtreler
# ana_strateji = st.selectbox("1️⃣ Ana Strateji", 
#                             sorted(df_filtered["Ana Strateji"].dropna().unique()),
#                             index=None,
#                             placeholder="Ana Stratejiyi Seçin")



aktif_ceyrek = "Hedef " + aktif_ceyrek
ana_stratejiler = sorted(
    df_filtered.loc[df_filtered[aktif_ceyrek].notna(), "Ana Strateji"]
    .dropna()
    .unique()
)

moduller = ["Süreç Kararları","Toplantı Kararları","Diğer Kararlar","KPI"]
modul_sec = st.selectbox("Modül Seç",options=moduller, index=None)


if modul_sec == "KPI":
    ana_strateji = st.selectbox("Ana Strateji Seç", options=ana_stratejiler, index=None)
    
    if ana_strateji:
        df_amac = df_filtered[
            (df_filtered["Ana Strateji"] == ana_strateji) &
            (df_filtered[aktif_ceyrek].notna())
        ]
        # df_amac = df_filtered[df_filtered["Ana Strateji"] == ana_strateji]
        stratejik_amac = st.selectbox("2️⃣ Stratejik Amaç",
                                      sorted(df_amac["Stratejik Amaç"].dropna().unique()),
                                      index=None,
                                      placeholder="Stratejik Amacı Seçin")
    else:
        stratejik_amac = None
    
    if stratejik_amac:
        df_hedef = df_amac[df_amac["Stratejik Amaç"] == stratejik_amac]
        stratejik_hedef = st.selectbox("3️⃣ Stratejik Hedef", 
                                       sorted(df_hedef["Stratejik Hedef"].dropna().unique()), 
                                       index=None,
                                       placeholder="Stratejik Hedefi Seçin")
    else:
        stratejik_hedef = None
    
    if stratejik_hedef:
        df_faaliyet = df_hedef[df_hedef["Stratejik Hedef"] == stratejik_hedef]
        selected_kpi = st.selectbox("4️⃣ Faaliyet", 
                                    sorted(df_faaliyet["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"].dropna().unique()),
                                    index=None,
                                    placeholder="Gerçekleştirilecek Faaliyeti Seçin")
    else:
        selected_kpi = None
    
    if not selected_kpi:
        st.stop()
    
    kpi_row_idx = df[df["Hedefe Ulaşmak İçin Gerçekleştirilecek Faaliyetler"] == selected_kpi].index[0]
    
    
    if selected_kpi != st.session_state.last_selected_kpi:
        st.session_state.durum = df.at[kpi_row_idx, "Durum"] if pd.notna(df.at[kpi_row_idx, "Durum"]) else ""
        st.session_state.aciklama = df.at[kpi_row_idx, "Açıklama"] if pd.notna(df.at[kpi_row_idx, "Açıklama"]) else ""
        tarih_deger = df.at[kpi_row_idx, "Önerilen Yeni Tarih"]
        st.session_state.yeni_tarih = pd.to_datetime(tarih_deger).date() if pd.notna(tarih_deger) else None
        st.session_state.last_selected_kpi = selected_kpi
    
    st.subheader("📝 Güncelleme Formu")
    
    refDegerHedef = df.loc[kpi_row_idx, aktif_ceyrek] 
    refDegerHedef = float(refDegerHedef)
    
    refDegerStr = df.loc[kpi_row_idx, 'Hedef Ölçüsü'] 
    if refDegerStr == "Oran" or refDegerStr == "Yüzde":
        refDeger = st.number_input(f"{refDegerStr} referans değerini girin",
                               min_value=0.0,
                               max_value=1.0,
                               step=0.01)
    else:
        refDeger = st.number_input(f"{refDegerStr} referans değerini girin",
                               min_value=0.0,
                               max_value=100.0,
                               step=0.1)
    # refDeger = round(refDeger, 4)
    refDeger = float(f"{refDeger:.2f}")
    
    
    if refDeger < refDegerHedef:
        durum = st.selectbox("Durum", 
                         ["Tamamlanmadı", "Ertelendi", "İptal Edildi"],
                         key="durum",
                         index=None,
                         placeholder="Durum Seçin")
    else:
        durum = "Tamamlandı"
        st.text_input("Durum", value=durum, disabled=True)
    
    
    
    aciklama = st.text_area("Açıklama / Gerekçe", key="aciklama")
    tarih_gir = st.checkbox("📅 Yeni hedef tarihi girmek istiyorum", value=st.session_state.yeni_tarih is not None)
    if tarih_gir:
        yeni_tarih = st.date_input("Yeni hedef tarih", value=st.session_state.yeni_tarih or datetime.today(), key="yeni_tarih")
    else:
        yeni_tarih = None
    if "Kanıt" in df.columns:
        kanit_var = df.at[kpi_row_idx, "Kanıt"]
        if pd.notna(kanit_var):
            st.info(f"📎 Daha önce yüklenen dosya: **{kanit_var}**")
    
    st.markdown('<p style="color:red; font-weight:bold; margin-bottom:0px;">📎 Kanıt Belgesi (ZORUNLU)</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["pdf", "docx", "xlsx","csv","xls"])
    
    # BURADA KALDIK!!! YENİ TARİH GÜNCELLEME OLACAK !! MAİLİNG OLACAK !! Q1 Q2 Q3 RAPORLAMA OLACAK!!
    # 
    
    
    if st.button("📩 Güncelle ve Kaydet"):
        if uploaded_file is None:
            st.error("❗ Lütfen zorunlu dosyayı yükleyin!")
        else:
            df.at[kpi_row_idx, "Durum"] = durum
            df.at[kpi_row_idx, "Açıklama"] = aciklama
            df.at[kpi_row_idx, "Güncelleme Tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if tarih_gir and yeni_tarih:
                df.at[kpi_row_idx, "Önerilen Yeni Tarih"] = yeni_tarih.strftime("%Y-%m-%d")
        
            if uploaded_file:
                os.makedirs(KANIT_KLASORU, exist_ok=True)
                doc_name = uploaded_file.name
                with open(os.path.join(KANIT_KLASORU, doc_name), "wb") as f:
                    f.write(uploaded_file.read())
                df.at[kpi_row_idx, "Kanıt"] = doc_name
        
            df.to_excel(KPI_DOSYA, sheet_name=KPI_SAYFA, index=False)
        
            log_kaydi = {
                "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Kullanıcı": st.session_state.kullanici,
                "KPI Adı": selected_kpi,
                "Durum": durum,
                "Açıklama": aciklama,
                "Yeni Tarih": yeni_tarih.strftime("%Y-%m-%d") if tarih_gir and yeni_tarih else "",
                "Yüklenen Dosya": uploaded_file.name if uploaded_file else ""
            }
            log_df = pd.DataFrame([log_kaydi])
            if os.path.exists(LOG_DOSYA):
                mevcut_log = pd.read_excel(LOG_DOSYA)
                tum_log = pd.concat([mevcut_log, log_df], ignore_index=True)
            else:
                tum_log = log_df
            tum_log.to_excel(LOG_DOSYA, index=False)
        
            st.success("✅ Güncelleme ve log başarıyla kaydedildi!")
elif modul_sec == "Süreç Kararları" or modul_sec == "Toplantı Kararları" or modul_sec == "Diğer Kararlar":

    
    aksiyon_df = pd.read_excel(TEV_AKSIYON)
    
    aksiyon_sec = aksiyon_df["İçerik"]
    aksiyon = st.selectbox("Aksiyon Seç", options=aksiyon_sec, index=None)
    if aksiyon:
        kullanıcılar = pd.read_excel(TEV_CALISAN)
        aksiyon_sorumlu_kisi = aksiyon_df.loc[aksiyon_df["İçerik"] == aksiyon, "Sorumlu Kişi"].values
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
                
                
                
                
                aciklama = st.text_area("Açıklama giriniz")
    st.stop()
        # TERMİN TARİHİ GELECEK
        # YAPILDI YAPILMADI GELECEK 
        # SORUMLU KİŞİ ALTINDAKİ KİŞİYE ATAYABİLİR
        # YAPILDI İSE BELGE YÜKLE
        # AÇIKLAMA ALANI
        # YAPILMADI İSE YENİ TARİH ÖNER. BİR ÜST BİRİME GİDER.
        # 
