import streamlit as st
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np

# Load dataset
data = pd.read_excel('bs_dan_kr_stunting(AutoRecovered).xlsx')

# Convert gender column 'JK' to numeric values
data['JK'] = data['JK'].replace({'P': 0, 'L': 1})  # Assuming 'L' represents males

# Train the Naive Bayes classifier for Scenario 3
X3 = data[['ZS_BB/U', 'ZS_TB/U', 'ZS_BB/TB']]
y3 = data['TB/U']
nb3 = GaussianNB()
nb3.fit(X3, y3)

# Train the Naive Bayes classifier for Scenario 4
X4 = data[['Berat', 'Tinggi', 'JK', 'ZS_TB/U']]
y4 = data['TB/U']
nb4 = GaussianNB()
nb4.fit(X4, y4)

# Train the Naive Bayes classifier for Scenario 2
X2 = data[['Berat', 'Tinggi', 'JK']]
y2 = data['TB/U']
nb2 = GaussianNB()
nb2.fit(X2, y2)

# Train the Naive Bayes classifier for Scenario 2
X1 = data[['Tinggi', 'ZS_TB/U', 'ZS_BB/U']]
y1 = data['TB/U']
nb1 = GaussianNB()
nb1.fit(X2, y2)
# Streamlit app
st.title("Stunting Prediction App")
st.write("""
Predict the severity of stunting based on Z-scores and other factors.
""")

# Sidebar for scenario selection
scenario = st.sidebar.selectbox("Choose a Scenario:", ["Scenario 3", "Scenario 4", "Scenario 2", "Scenario 1"])

if scenario == "Scenario 3":
    # User input for Scenario 3
    zs_bb_u = st.number_input("Enter ZS_BB/U:", min_value=-5.0, max_value=5.0, value=0.0, step=0.01)
    zs_tb_u = st.number_input("Enter ZS_TB/U:", min_value=-5.0, max_value=5.0, value=0.0, step=0.01)
    zs_bb_tb = st.number_input("Enter ZS_BB/TB:", min_value=-5.0, max_value=5.0, value=0.0, step=0.01)
    
    # Predict and display result for Scenario 3
    if st.button("Predict for Scenario 3"):
        prediction = nb3.predict(np.array([[zs_bb_u, zs_tb_u, zs_bb_tb]]))[0]
        st.subheader(f"The predicted stunting severity for Scenario 3 is: {prediction}")

elif scenario == "Scenario 4":
    # User input for Scenario 4
    berat = st.number_input("Enter Weight (Berat):", min_value=0.0, max_value=50.0, value=10.0, step=1.00)
    tinggi = st.number_input("Enter Height (Tinggi):", min_value=30.0, max_value=200.0, value=100.0, step=0.01)
    jk = st.selectbox("Select Gender (JK) 0 == 'P (Perempuan)', 1 == 'L (Laki-Laki)' :", [0, 1])
    zs_tb_u = st.number_input("Enter ZS_TB/U:", min_value=-5.0, max_value=5.0, value=0.0, step=1.00)

    # Predict and display result for Scenario 4
    if st.button("Predict for Scenario 4"):
        prediction = nb4.predict(np.array([[berat, tinggi, jk, zs_tb_u]]))[0]
        st.subheader(f"Prediksi Tingkat Keparan indikasi Stunting: {prediction}")

elif scenario == "Scenario 2":
    berat = st.number_input("Enter Weight (Berat):", min_value=0.0, max_value=50.0, value=10.0, step=1.00)
    tinggi = st.number_input("Enter Height (Tinggi):", min_value=30.0, max_value=200.0, value=100.0, step=0.01)
    jk = st.selectbox("Select Gender (JK) 0 == 'P (Perempuan)', 1 == 'L (Laki-Laki)' :", [0, 1])

    # Predict and display result for Scenario 4
    if st.button("Predict for Scenario 2"):
        prediction = nb2.predict(np.array([[berat, tinggi, jk]]))[0]
        st.subheader(f"Prediksi Tingkat Keparan indikasi Stunting: {prediction}")

elif scenario == "Scenario 1":
    tinggi = st.number_input("Enter Height (Tinggi):", min_value=30.0, max_value=200.0, value=100.0, step=0.01)
    zs_bb_u = st.number_input("Enter ZS_BB/U:", min_value=-5.0, max_value=5.0, value=0.0, step=0.01)
    zs_tb_u = st.number_input("Enter ZS_TB/U:", min_value=-5.0, max_value=5.0, value=0.0, step=0.01)

    # Predict and display result for Scenario 4
    if st.button("Predict for Scenario 1"):
        prediction = nb2.predict(np.array([[tinggi, zs_bb_u, zs_tb_u]]))[0]
        st.subheader(f"Prediksi Tingkat Keparan indikasi Stunting: {prediction}")

# Additional information
st.write("""
---
## What is this app about?

This app predicts the severity of stunting in children based on various factors and Z-scores. 
Choose a scenario from the sidebar and provide the required inputs to get the prediction.
""")

# Embed the calculator from the web using iframe
st.write("""
## Z-Score Calculator
Embed from https://psgbalita.com/kalkulator
""")
html_code = """
<iframe src="https://psgbalita.com/kalkulator" width="1000" height="600"></iframe>
"""
st.write(html_code, unsafe_allow_html=True)
