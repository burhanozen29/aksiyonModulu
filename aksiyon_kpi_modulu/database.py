# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:09:34 2025

@author: bozen
"""

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["aksiyon_modul"]
tev_calisan = db["tev_calisan"]
