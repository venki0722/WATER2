from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('linear_regression_model.pkl')

# Get the feature columns from the training data (crucial for consistent input)
# This assumes X_train was defined and is available in the kernel state.
# If X_train was not available, we would need to regenerate it or infer column names.
# For this example, we'll hardcode based on the previous cell's output or assume it's accessible.
# In a real-world scenario, you might save these columns alongside the model.
# The columns are: 'temperature', 'rainfall', 'humidity', 'crop_rice', 'crop_wheat', 'soil_loamy', 'soil_sandy'

# To make this robust, we should derive the columns dynamically from the `x_encoded` DataFrame
# that was created during training. If `x_encoded` is not available at runtime of the API,
# it should be recreated with dummy data or saved as a separate artifact.
# For now, let's list them based on previous execution to demonstrate.
expected_model_columns = [
    'temperature',
    'rainfall',
    'humidity',
    'crop_rice',
    'crop_wheat',
    'soil_loamy',
    'soil_sandy'
]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        # Prepare input data for the model
        # Create a DataFrame with the correct structure
        input_df = pd.DataFrame({
            'temperature': [data['temperature']],
            'rainfall': [data['rainfall']],
            'humidity': [data['humidity']]
        })

        # Initialize all one-hot encoded columns to False
        for col in ['crop_rice', 'crop_wheat', 'soil_loamy', 'soil_sandy']:
            input_df[col] = False
        
        # Set the appropriate one-hot encoded columns to True based on input 'crop' and 'soil'
        if 'crop' in data:
            crop_col = f"crop_{data['crop']}"
            if crop_col in input_df.columns:
                input_df[crop_col] = True
        
        if 'soil' in data:
            soil_col = f"soil_{data['soil']}"
            if soil_col in input_df.columns:
                input_df[soil_col] = True
        
        # Ensure the order of columns matches what the model was trained on
        input_df = input_df[expected_model_columns]

        # Make prediction
        prediction = model.predict(input_df)

        return jsonify({'predicted_water': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# To run this Flask app in a Colab environment, you typically need to use ngrok
# or a similar tool to expose the local server. The following line is for direct execution
# and will block the notebook. In a real scenario, you might run this as a separate script.
# For demonstration purposes, you can comment this out and use `!flask run` in a terminal
# or use a tool like `flask_ngrok` for Colab if you want to test it directly.

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

