import streamlit as st
import pandas as pd
from datetime import datetime

# Load all the required data here (as shown previously)
df_bb_u_laki = pd.read_excel("Anak Laki BB_U umur 0-60 bulan.xlsx")
df_bb_u_perempuan = pd.read_csv("Berat_Badan_Menurut_Umur_Perempuan_0-60 bulan.csv")
# Load the data for weight according to height for ages 0-24 months
df_bb_pb_laki_0_24 = pd.read_csv("Berat_Badan_Menurut_Panjang_Badan BB per PB_Laki-laki_Umur 0-24.csv")
df_bb_pb_perempuan_0_24 = pd.read_csv("Berat_Badan_Menurut_Panjang_Badan_Perempuan_0-24 bulan .csv")
# Load the data for weight according to height for ages 24-60 months
df_bb_tb_laki_24_60 = pd.read_csv("Berat_Badan_Menurut_Tinggi_Badan_ BB per TB_umur 24-60.csv")
df_bb_tb_perempuan_24_60 = pd.read_csv("Berat_badan_menurut_Tinggi_Badan_Perempuan_umur 24-60 bulan.csv")
# Load the data for boys aged 0-24 months TB/U
df_0_24_laki = pd.read_excel("Anak_laki_PB_U_umur_0-24_pengukuran_terlentang.xlsx")

# Load the data for boys aged 24-60 months TB/U
df_24_60_laki = pd.read_excel("Tinggi_Badan_Umur_24_60_Bulan_Laki.xlsx")

# Load the data for girls aged 0-24 months
df_0_24_perempuan = pd.read_csv("Panjang_Badan_Menurut_Umur_Perempuan_0-24 bulan.csv")

# Load the data for girls aged 24-60 months
df_24_60_perempuan = pd.read_csv("Tinggi_Badan_menurut_umur_Perempuan_24-60 umur_pengukuran berdiri.csv")


def z_score_calculator(height, weight, age, gender, calculation_type):
    """
    Calculate the Z-Score for different parameters.
    
    Parameters:
    - height: Height of the child
    - weight: Weight of the child
    - age: Age of the child in months
    - gender: Gender of the child ("Laki-laki" or "Perempuan")
    - calculation_type: Type of calculation ("TB/U", "BB/U", "BB/TB")
    
    Returns:
    - Z-Score for the specified parameter
    """
    
    if calculation_type == "TB/U":
        if age <= 24:
            df = df_0_24_laki if gender == "Laki-laki" else df_0_24_perempuan
        else:
            df = df_24_60_laki if gender == "Laki-laki" else df_24_60_perempuan
        data_value = height

    elif calculation_type == "BB/U":
        df = df_bb_u_laki if gender == "Laki-laki" else df_bb_u_perempuan
        data_value = weight
    
    elif calculation_type == "BB/TB":
        if age <= 24:
            df = df_bb_pb_laki_0_24 if gender == "Laki-laki" else df_bb_pb_perempuan_0_24
        else:
            df = df_bb_tb_laki_24_60 if gender == "Laki-laki" else df_bb_tb_perempuan_24_60
        data_value = weight

    # Calculate the Z-Score
    median = df[df['Umur (bulan)'] == age]['Median'].values[0] if calculation_type == "BB/U" else df[df.columns[0]].iloc[(df[df.columns[0]]-data_value).abs().argsort()[:1]].values[0]
    if data_value < median:
        sd_below_median = df[df['Umur (bulan)'] == age]['-1 SD'].values[0] if calculation_type == "BB/U" else df[df[df.columns[0]] == median]['-1 SD'].values[0]
        z_score = (data_value - median) / (median - sd_below_median)
    else:
        sd_above_median = df[df['Umur (bulan)'] == age]['+1 SD'].values[0] if calculation_type == "BB/U" else df[df[df.columns[0]] == median]['+1 SD'].values[0]
        z_score = (data_value - median) / (sd_above_median - median)
    
    return z_score

def calculate_age(birth_date, measurement_date):
    delta = measurement_date - birth_date
    age_in_months = delta.days / 30.44
    return round(age_in_months)

st.title("Kalkulator Z-Score")

# Input fields
height = st.number_input("Masukkan Tinggi Badan (cm)", min_value=1.0, max_value=200.0, step=0.1)
weight = st.number_input("Masukkan Berat Badan (kg)", min_value=0.1, max_value=150.0, step=0.1)
birth_date = st.date_input("Tanggal Lahir")
measurement_date = st.date_input("Tanggal Pengukuran")
gender = st.selectbox("Pilih Jenis Kelamin", ["Laki-laki", "Perempuan"])
parameter = st.selectbox("Pilih Parameter", ["TB/U", "BB/U", "BB/TB"])

if st.button("Hitung Z-Score"):
    age = calculate_age(birth_date, measurement_date)
    z_score = z_score_calculator(height, weight, age, gender, parameter)
    st.write(f"Umur: {age} bulan")
    st.write(f"Z-Score: {z_score:.4f}")
