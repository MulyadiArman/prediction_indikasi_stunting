
import streamlit as st
import pandas as pd
from datetime import datetime

# Load data
data_laki_bb_pb = pd.read_csv("BB_TB/Berat_Badan_Menurut_Panjang_Badan BB per PB_Laki-laki_Umur 0-24.csv")
data_perempuan_bb_pb = pd.read_csv("BB_TB/Berat_Badan_Menurut_Panjang_Badan_Perempuan_0-24 bulan .csv")
data_laki_bb_tb = pd.read_csv("BB_TB/Berat_Badan_Menurut_Tinggi_Badan_ Laki-laki_BB per TB_umur 24-60.csv")
data_perempuan_bb_tb = pd.read_csv("BB_TB/Berat_badan_menurut_Tinggi_Badan_Perempuan_umur 24-60 bulan.csv")

def calculate_z_score_bb_tb(bb_anak, tb_anak, jenis_kelamin, umur):
    if jenis_kelamin == "Laki-laki":
        if umur <= 24:
            data = data_laki_bb_pb
        else:
            data = data_laki_bb_tb
    else:
        if umur <= 24:
            data = data_perempuan_bb_pb
        else:
            data = data_perempuan_bb_tb
            
    row = data[data["Tinggi Badan (cm)"] == round(tb_anak)]
    bb_median = row["Median"].values[0]
    
    if bb_anak < bb_median:
        sd_below = row["-1 SD"].values[0]
        z_score = (bb_anak - bb_median) / (bb_median - sd_below)
    else:
        sd_above = row["+1 SD"].values[0]
        z_score = (bb_anak - bb_median) / (sd_above - bb_median)
        
    return z_score

from datetime import datetime
def calculate_age(tanggal_lahir, tanggal_pengukuran):
    delta = tanggal_pengukuran - tanggal_lahir
    age_in_months = delta.days // 30
    return age_in_months

# Streamlit UI
st.title("Kalkulator Z-score BB/TB Anak")
st.write("Silahkan masukkan data anak:")

# User input
bb_anak = st.number_input("Berat Badan Anak (kg)", min_value=0.0, step=0.1)
tb_anak = st.number_input("Tinggi Badan Anak (cm)", min_value=0.0, step=0.1)
tanggal_lahir = st.date_input("Tanggal Lahir Anak")
tanggal_pengukuran = st.date_input("Tanggal Pengukuran")
jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

# Calculate Z-score
if st.button("Hitung Z-score BB/TB"):
    umur = calculate_age(tanggal_lahir, tanggal_pengukuran)
    z_score = calculate_z_score_bb_tb(bb_anak, tb_anak, jenis_kelamin, umur)
    st.write(f"Umur anak dalam bulan: {umur} bulan")
    st.write(f"Z-score BB/TB anak adalah: {z_score:.2f}")

