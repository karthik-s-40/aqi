from flask import Flask, request, jsonify,render_template
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd
import joblib
import xgboost as xgb


app = Flask(__name__, static_folder='static', template_folder='templates')

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

# Load the old model
old_model = joblib.load("air_quality_model.pkl")

# Extract the actual XGBoost model
xgb_model = old_model.estimators_[0]  # Extract the first XGBoost estimator

# Save in XGBoost format
xgb_model.save_model("air_quality_model.json")


model = xgb.Booster()
model.load_model("air_quality_model.json")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    location = data.get("location")
    pollut = data.get("pollutant").strip().upper()
    
    coordinates = get_lat_lon_if_india(location)
    if pollut in ["PM2.5", "PM25"]:  # ✅ Handle cases where "." might be removed
        pollut = "PM2.5"
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
    
    max_pollutant = float(predicted_df["Maximum Pollutant level"].iloc[0])
    min_pollutant = float(predicted_df["Minimum Pollutant level"].iloc[0])
    avg_pollutant = float(predicted_df["Average Pollutant level"].iloc[0])

    def get_aqi_status(value):
        if value <= 50:
            return "Good"
        elif 51 <= value <= 100:
            return "Moderate"
        elif 101 <= value <= 200:
          return "Unhealthy for Sensitive Groups"
        elif 201 <= value <= 300:
           return "Unhealthy"
        elif 301 <= value <= 400:
            return "Very Unhealthy"
        else:
         return "Hazardous"

# Get AQI statuses for min, avg, and max pollutant levels
    min_status = get_aqi_status(min_pollutant)
    avg_status = get_aqi_status(avg_pollutant)
    max_status = get_aqi_status(max_pollutant)

# Final AQI status prioritizing the worst-case scenario
    if max_status == "Hazardous":
        aqi_status = "Hazardous"
    elif max_status == "Very Unhealthy":
        aqi_status = "Very Unhealthy"
    elif max_status == "Unhealthy":
        aqi_status = "Unhealthy"
    elif avg_status == "Unhealthy for Sensitive Groups":
        aqi_status = "Unhealthy for Sensitive Groups"
    elif avg_status == "Moderate":
        aqi_status = "Moderate"
    else:
        aqi_status = "Good"
    
    return jsonify({
    "Minimum Pollutant Level": format(predicted_df["Minimum Pollutant level"].iloc[0], ".2f"),
    "Maximum Pollutant Level": format(predicted_df["Maximum Pollutant level"].iloc[0], ".2f"),
    "Average Pollutant Level": format(avg_pollutant, ".2f"),
    "AQI Status": str(aqi_status)  # Ensure it's a string
})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
