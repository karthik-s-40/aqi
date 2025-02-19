import joblib
import numpy as np
import pandas as pd
import sklearn  # Import scikit-learn to check version

# Print scikit-learn version
print("Scikit-learn Version:", sklearn.__version__)

# Load model and scaler
model = joblib.load("air_quality_model.pkl")
scaler = joblib.load("scaler.pkl")

print("Model Loaded:", type(model))
print("Scaler Loaded:", type(scaler))

# Test data for prediction (latitude, longitude, pollutant_id)
test_data = np.array([[12.9716, 77.5946, 5]])  # Example location and pollutant

# Convert to DataFrame
test_df = pd.DataFrame(test_data, columns=["latitude", "longitude", "pollutant_id"])

# Scale the latitude and longitude
scaled_values = scaler.transform(test_df.iloc[:, :2])
scaled_df = pd.DataFrame(scaled_values, columns=["latitude", "longitude"])
scaled_df["pollutant_id"] = test_df["pollutant_id"].values

# Make a prediction
prediction = model.predict(scaled_df)
print("Predicted AQI Levels:", prediction)
