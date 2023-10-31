import streamlit as st
from datetime import datetime
import pandas as pd

# Load data (pastikan Anda mengganti path sesuai dengan lokasi file Anda)
laki_0_24 = pd.read_excel("Anak_laki_PB_U_umur_0-24_pengukuran_terlentang.xlsx")
perempuan_0_24 = pd.read_csv("Panjang_Badan_Menurut_Umur_Perempuan_0-24 bulan.csv")
perempuan_24_60 = pd.read_csv("Tinggi_Badan_menurut_umur_Perempuan_24-60 umur_pengukuran berdiri.csv")
laki_24_60 = pd.read_excel("Tinggi_Badan_Umur_24_60_Bulan_Laki.xlsx")

# Fungsi menghitung Z-Score (sama dengan yang dibuat sebelumnya)
def calculate_z_score(tinggi_anak, jenis_kelamin, tanggal_lahir, tanggal_pengukuran):
    # ... (kode yang sama)
    # Menghitung umur anak dalam bulan
    umur_bulan = (tanggal_pengukuran.year - tanggal_lahir.year) * 12 + tanggal_pengukuran.month - tanggal_lahir.month
    
    # Memilih tabel yang sesuai berdasarkan jenis kelamin dan umur anak
    if jenis_kelamin == "laki-laki":
        if umur_bulan <= 24:
            data = laki_0_24
        else:
            data = laki_24_60
    else:  # perempuan
        if umur_bulan <= 24:
            data = perempuan_0_24
        else:
            data = perempuan_24_60
            
    # Mengambil data tinggi median, -1SD, dan +1SD berdasarkan umur anak
    row = data[data['Umur (bulan)'] == umur_bulan].iloc[0]
    tb_median = row['Median']
    tb_minus_1sd = row['-1 SD']
    tb_plus_1sd = row['+1 SD']
    
    # Menghitung Z-Score berdasarkan formula yang diberikan
    if tinggi_anak < tb_median:
        z_score = (tinggi_anak - tb_median) / (tb_median - tb_minus_1sd)
    else:
        z_score = (tinggi_anak - tb_median) / (tb_plus_1sd - tb_median)
    
    return z_score

st.title("Kalkulator Z-Score Tinggi Badan Anak")

# Input dari pengguna
tinggi_anak = st.number_input("Tinggi Badan Anak (cm)", min_value=0.0, step=0.1)
jenis_kelamin = st.selectbox("Jenis Kelamin", ["laki-laki", "perempuan"])
tanggal_lahir = st.date_input("Tanggal Lahir Anak")
tanggal_pengukuran = st.date_input("Tanggal Pengukuran")

# Menghitung Z-Score ketika tombol di-klik
if st.button("Hitung Z-Score"):
    z_score = calculate_z_score(tinggi_anak, jenis_kelamin, tanggal_lahir, tanggal_pengukuran)
    st.write(f"Z-Score: {z_score:.2f}")

