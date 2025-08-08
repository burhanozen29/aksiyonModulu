# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:09:44 2025

@author: bozen
"""

from aksiyon_kpi_modulu.database import tev_calisan

def kullanici_dogrula(kullanici_adi, sifre):
    user = tev_calisan.find_one({"Kullanıcı": kullanici_adi, "Şifre": sifre})
    if user:
        birimler = user.get("Birim", "")
        rol = user.get("Rol", "")
        bagli_birim = user.get("Bağlı Kişi Birim","")
        bagli_kisi = user.get("Bağlı Kişi","")
        isim = user.get("İsim","")
        birim_listesi = [b.strip() for b in birimler.split(",")] if isinstance(birimler, str) else []
        return {"birimler": birim_listesi, "rol": rol, "bagli_birim":bagli_birim, "bagli_kisi":bagli_kisi,"isim":isim}
    return None
