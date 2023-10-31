
import streamlit as st
import pandas as pd
from datetime import datetime

# Load data
data_laki_pb_u = pd.read_excel("/path/to/Anak_laki_PB_U_umur_0-24_pengukuran_terlentang.xlsx")
data_perempuan_pb_u = pd.read_csv("/path/to/Panjang_Badan_Menurut_Umur_Perempuan_0-24 bulan.csv")
data_perempuan_tb_u = pd.read_csv("/path/to/Tinggi_Badan_menurut_umur_Perempuan_24-60 umur_pengukuran berdiri.csv")
data_laki_tb_u = pd.read_excel("/path/to/Tinggi_Badan_Umur_24_60_Bulan_Laki.xlsx")

def calculate_age(tanggal_lahir, tanggal_pengukuran):
    delta = tanggal_pengukuran - tanggal_lahir
    age_in_months = delta.days // 30
    return age_in_months

def calculate_z_score(tb_anak, umur, jenis_kelamin):
    if jenis_kelamin == "Laki-laki":
        if umur <= 24:
            data = data_laki_pb_u
        else:
            data = data_laki_tb_u
    else:
        if umur <= 24:
            data = data_perempuan_pb_u
        else:
            data = data_perempuan_tb_u
            
    row = data[data["Umur (bulan)"] == umur]
    tb_median = row["Median"].values[0]
    
    if tb_anak < tb_median:
        sd_below = row["-1 SD"].values[0]
        z_score = (tb_anak - tb_median) / (tb_median - sd_below)
    else:
        sd_above = row["+1 SD"].values[0]
        z_score = (tb_anak - tb_median) / (sd_above - tb_median)
        
    return z_score

# Streamlit UI
st.title("Kalkulator Z-score TB/U Anak")
st.write("Silahkan masukkan data anak:")

# User input
tb_anak = st.number_input("Tinggi/Panjang Badan Anak (cm)", min_value=0.0, step=0.1)
tanggal_lahir = st.date_input("Tanggal Lahir Anak")
tanggal_pengukuran = st.date_input("Tanggal Pengukuran")
jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

# Calculate Z-score
if st.button("Hitung Z-score"):
    umur = calculate_age(tanggal_lahir, tanggal_pengukuran)
    z_score = calculate_z_score(tb_anak, umur, jenis_kelamin)
    st.write(f"Umur anak dalam bulan: {umur} bulan")
    st.write(f"Z-score TB/U anak adalah: {z_score:.2f}")

