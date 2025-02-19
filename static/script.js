// ✅ Ensure only one event listener for form submission
document.getElementById('prediction-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const location = document.getElementById('location').value;
    let pollutant = document.getElementById('pollutant').value.trim().toUpperCase();

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location: location, pollutant: pollutant })
    })
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data); // ✅ Debugging: Check API response

        if (data.error) {
            alert(data.error);
        } else {
            updateUIWithResults(
                data["Minimum Pollutant Level"], 
                data["Maximum Pollutant Level"], 
                data["Average Pollutant Level"], 
                data["AQI Status"]
            );
        }
    })
    .catch(error => console.error('Error:', error));
});

// ✅ Update UI with Min, Max, and Avg AQI
function updateUIWithResults(minAQI, maxAQI, avgAQI, aqiStatus) {
    if (!minAQI || !maxAQI || !avgAQI) {
        console.error("Error: AQI values are undefined!");
        alert("Prediction failed. Please check your input.");
        return;
    }

    document.getElementById('aqi-min').textContent = `Min AQI: ${minAQI}`;
    document.getElementById('aqi-max').textContent = `Max AQI: ${maxAQI}`;
    document.getElementById('aqi-value').textContent = `Avg AQI: ${avgAQI}`;
    document.getElementById('aqi-description').textContent = aqiStatus;

    const resultSection = document.getElementById('result-section');
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}
