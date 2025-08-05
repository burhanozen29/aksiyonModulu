# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:09:56 2025

@author: bozen
"""
from datetime import datetime

def aktif_ceyrek_bul():
    ay = datetime.today().month
    yil = datetime.today().year
    if yil == 2025:
        if ay in [1, 2, 3]: return "2025 Q1"
        elif ay in [4, 5, 6]: return "2025 Q2"
        elif ay in [7, 8, 9]: return "2025 Q3"
        elif ay in [10, 11, 12]: return "2025 Q4"
    elif yil == 2026:
        if ay in [1, 2, 3]: return "2026 Q1"
        elif ay in [4, 5, 6]: return "2026 Q2"
        elif ay in [7, 8, 9]: return "2026 Q3"
        elif ay in [10, 11, 12]: return "2026 Q4"
    elif yil == 2027:
        if ay in [1, 2, 3]: return "2027 Q1"
        elif ay in [4, 5, 6]: return "2027 Q2"
        elif ay in [7, 8, 9]: return "2027 Q3"
        elif ay in [10, 11, 12]: return "2027 Q4"
    return None
