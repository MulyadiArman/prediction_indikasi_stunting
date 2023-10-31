
import streamlit as st
import pandas as pd
from datetime import datetime

# Load data
data_laki_bb_u = pd.read_excel("BBanak/Anak Laki BB_U umur 0-60 bulan.xlsx")
data_perempuan_bb_u = pd.read_csv("BBanak/Berat_Badan_Menurut_Umur_Perempuan_0-60 bulan.csv")

def calculate_age(tanggal_lahir, tanggal_pengukuran):
    delta = tanggal_pengukuran - tanggal_lahir
    age_in_months = delta.days // 30
    return age_in_months

def calculate_z_score_bb_u(bb_anak, umur, jenis_kelamin):
    if jenis_kelamin == "Laki-laki":
        data = data_laki_bb_u
    else:
        data = data_perempuan_bb_u
            
    row = data[data["Umur (bulan)"] == umur]
    bb_median = row["Median"].values[0]
    
    if bb_anak < bb_median:
        sd_below = row["-1 SD"].values[0]
        z_score = (bb_anak - bb_median) / (bb_median - sd_below)
    else:
        sd_above = row["+1 SD"].values[0]
        z_score = (bb_anak - bb_median) / (sd_above - bb_median)
        
    return z_score

# Streamlit UI
st.title("Kalkulator Z-score BB/U Anak")
st.write("Silahkan masukkan data anak:")

# User input
bb_anak = st.number_input("Berat Badan Anak (kg)", min_value=0.0, step=0.1)
tanggal_lahir = st.date_input("Tanggal Lahir Anak")
tanggal_pengukuran = st.date_input("Tanggal Pengukuran")
jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

# Calculate Z-score
if st.button("Hitung Z-score BB/U"):
    umur = calculate_age(tanggal_lahir, tanggal_pengukuran)
    z_score = calculate_z_score_bb_u(bb_anak, umur, jenis_kelamin)
    st.write(f"Umur anak dalam bulan: {umur} bulan")
    st.write(f"Z-score BB/U anak adalah: {z_score:.2f}")

