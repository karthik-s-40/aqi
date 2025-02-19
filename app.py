from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

def get_lat_lon_if_india(location):
    geolocator = Nominatim(user_agent="geo_locator")
    location_data = geolocator.geocode(location, exactly_one=True, country_codes="IN")  
    
    if location_data:
        return [location_data.latitude, location_data.longitude]
    return None

pollutid = {
    'CO': 0, 'CARBON MONOXIDE': 0,
    'NH3': 1, 'AMMONIA': 1,
    'NO2': 2, 'NITROGEN DIOXIDE': 2,
    'OZONE': 3, 'O3': 3,
    'PM10': 4, 'PARTICULATE MATTER 10': 4,
    'PM2.5': 5, 'PARTICULATE MATTER 2.5': 5,
    'SO2': 6, 'SULFUR DIOXIDE': 6
}

# Load the trained model and scaler
model = joblib.load("air_quality_model.pkl")
sc = joblib.load("scaler.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    location = data.get("location")
    pollut = data.get("pollutant").strip().upper()
    
    coordinates = get_lat_lon_if_india(location)
    if not coordinates:
        return jsonify({"error": "Location not found in India"}), 400
    
    if pollut not in pollutid:
        return jsonify({"error": "Invalid pollutant"}), 400
    
    pollutant_id = pollutid[pollut]
    locat = [coordinates + [pollutant_id]]
    
    feature_names = ["latitude", "longitude", "pollutant_id"]
    sample_test_df = pd.DataFrame(locat, columns=feature_names)
    
    # Scale latitude & longitude
    scaled_values = sc.transform(sample_test_df.iloc[:, :2])
    scaled_df = pd.DataFrame(scaled_values, columns=["latitude", "longitude"])
    scaled_df["pollutant_id"] = sample_test_df["pollutant_id"].values
    
    # Predict AQI levels
    prediction = model.predict(scaled_df).reshape(1, -1)
    att = ["Minimum Pollutant level", "Maximum Pollutant level", "Average Pollutant level"]
    predicted_df = pd.DataFrame(prediction, columns=att)
    avg_pollutant = predicted_df["Average Pollutant level"].iloc[0]
    
    aqi_status = "Unhealthy" if avg_pollutant > 100 else "Satisfactory" if avg_pollutant >= 51 else "Healthy"
    
    return jsonify({
    "Minimum Pollutant Level": format(predicted_df["Minimum Pollutant level"].iloc[0], ".2f"),
    "Maximum Pollutant Level": format(predicted_df["Maximum Pollutant level"].iloc[0], ".2f"),
    "Average Pollutant Level": format(avg_pollutant, ".2f"),
    "AQI Status": str(aqi_status)  # Ensure it's a string
})



if __name__ == "__main__":
    app.run(debug=True)
