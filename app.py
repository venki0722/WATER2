import streamlit as st
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('linear_regression_model.pkl')

# Title
st.title("💧 Water Prediction App")

# Inputs
temperature = st.number_input("Temperature", min_value=0.0)
rainfall = st.number_input("Rainfall", min_value=0.0)
humidity = st.number_input("Humidity", min_value=0.0)

crop = st.selectbox("Select Crop", ["rice", "wheat"])
soil = st.selectbox("Select Soil", ["loamy", "sandy"])

# Predict button
if st.button("Predict Water Requirement"):
    try:
        # Create input dataframe
        input_df = pd.DataFrame({
            'temperature': [temperature],
            'rainfall': [rainfall],
            'humidity': [humidity],
            'crop_rice': [crop == "rice"],
            'crop_wheat': [crop == "wheat"],
            'soil_loamy': [soil == "loamy"],
            'soil_sandy': [soil == "sandy"]
        })

        # Prediction
        prediction = model.predict(input_df)

        st.success(f"💧 Predicted Water Needed: {prediction[0]}")

    except Exception as e:
        st.error(f"Error: {e}")
