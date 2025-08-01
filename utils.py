# utils.py

import pandas as pd
import os
from datetime import datetime
from config import KULLANICI_DOSYA

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
        elif ay in [7, 8, 9]:
            return "2026 Q3"
        elif ay in [10, 11, 12]:
            return "2026 Q4"
    elif yil == 2027:
        if ay in [1, 2, 3]:
            return "2027 Q1"
        elif ay in [4, 5, 6]:
            return "2027 Q2"
        elif ay in [7, 8, 9]:
            return "2027 Q3"
        elif ay in [10, 11, 12]:
            return "2027 Q4"
    return None

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
