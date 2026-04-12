import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# Load model
model = joblib.load('linear_regression_model.pkl')

# Page config (dashboard look)
st.set_page_config(page_title="Water Dashboard", layout="wide")

st.title("💧 Smart Water Prediction Dashboard")

# Layout columns
col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("🌡 Temperature", min_value=0.0)
    rainfall = st.number_input("🌧 Rainfall", min_value=0.0)
    humidity = st.number_input("💨 Humidity", min_value=0.0)

with col2:
    crop = st.selectbox("🌾 Select Crop", ["rice", "wheat"])
    soil = st.selectbox("🪨 Select Soil", ["loamy", "sandy"])

# Predict button
if st.button("📊 Predict Water Requirement"):

    # Input dataframe
    input_df = pd.DataFrame({
        'temperature': [temperature],
        'rainfall': [rainfall],
        'humidity': [humidity],
        'crop_rice': [crop == "rice"],
        'crop_wheat': [crop == "wheat"],
        'soil_loamy': [soil == "loamy"],
        'soil_sandy': [soil == "sandy"]
    })

    prediction = model.predict(input_df)[0]

    st.success(f"💧 Predicted Water Needed: {prediction:.2f}")

    # ---------------- DASHBOARD SECTION ---------------- #

    st.subheader("📊 Analytics Dashboard")

    col3, col4 = st.columns(2)

    # 🔵 BAR GRAPH (Input vs Predicted impact view)
    with col3:
        bar_data = pd.DataFrame({
            "Factors": ["Temperature", "Rainfall", "Humidity", "Predicted Water"],
            "Values": [temperature, rainfall, humidity, prediction]
        })

        fig_bar = px.bar(
            bar_data,
            x="Factors",
            y="Values",
            title="Input vs Prediction Comparison"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # 🟠 PIE CHART (Contribution style view)
    with col4:
        pie_data = pd.DataFrame({
            "Category": ["Temperature", "Rainfall", "Humidity"],
            "Value": [temperature, rainfall, humidity]
        })

        fig_pie = px.pie(
            pie_data,
            names="Category",
            values="Value",
            title="Environmental Factors Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ---------------- EXTRA DASHBOARD CARD ---------------- #
    st.info("📌 Tip: Higher humidity and rainfall usually reduce water requirement.")
