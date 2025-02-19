// Create particles for animation
document.addEventListener('DOMContentLoaded', function() {
    const particlesContainer = document.getElementById('particles-container');
    const numberOfParticles = 50;
    
    // Generate particles
    for (let i = 0; i < numberOfParticles; i++) {
        createParticle();
    }
    
    function createParticle() {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Random particle properties
        const size = Math.random() * 15 + 5;
        const posX = Math.random() * window.innerWidth;
        const posY = Math.random() * window.innerHeight;
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 5;
        
        // Set particle style
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${posX}px`;
        particle.style.top = `${posY}px`;
        particle.style.background = `rgba(173, 216, 230, ${Math.random() * 0.4 + 0.1})`;
        particle.style.animationDuration = `${duration}s`;
        particle.style.animationDelay = `${delay}s`;
        
        particlesContainer.appendChild(particle);
        
        // Remove and create new particle after animation completes
        setTimeout(() => {
            particle.remove();
            createParticle();
        }, (duration + delay) * 1000);
    }
});

// Form submission handling
document.getElementById('prediction-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const location = document.getElementById('location').value;
    const pollutant = document.getElementById('pollutant').value;
    
    // This mock AQI calculation should be replaced with your actual API call
    // to your backend model when you integrate it
    const mockAQI = Math.floor(Math.random() * 300);
    
    // Example of how to call your backend API (commented out)
    /*
    fetch('your-backend-api-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            location: location,
            pollutant: pollutant
        })
    })
    .then(response => response.json())
    .then(data => {
        // Use the data from your model here
        const actualAQI = data.aqi;
        updateUIWithResults(actualAQI);
    })
    .catch(error => {
        console.error('Error:', error);
    });
    */
    
    // Instead of the above commented-out code, we're using mockAQI for now
    updateUIWithResults(mockAQI);
});

// Function to update UI with results
function updateUIWithResults(aqiValue) {
    let description, recommendations, position;
    
    // Determine AQI category and recommendations
    if (aqiValue <= 50) {
        description = "Good - Air quality is satisfactory, and air pollution poses little or no risk.";
        recommendations = [
            "You can enjoy outdoor activities.",
            "The air quality is ideal for most individuals."
        ];
        position = "8%";
    } else if (aqiValue <= 100) {
        description = "Moderate - Air quality is acceptable, but some pollutants may be a concern for sensitive individuals.";
        recommendations = [
            "Unusually sensitive people should consider reducing prolonged outdoor exertion.",
            "It's a good day for most people to be outside."
        ];
        position = "25%";
    } else if (aqiValue <= 150) {
        description = "Unhealthy for Sensitive Groups - May cause health effects for sensitive groups.";
        recommendations = [
            "People with heart or lung disease, older adults, and children should reduce prolonged or heavy exertion.",
            "Everyone else can enjoy outdoor activities."
        ];
        position = "42%";
    } else if (aqiValue <= 200) {
        description = "Unhealthy - May cause health effects for everyone, with more serious effects for sensitive groups.";
        recommendations = [
            "People with heart or lung disease, older adults, and children should avoid prolonged or heavy exertion.",
            "Everyone else should reduce prolonged or heavy exertion."
        ];
        position = "59%";
    } else if (aqiValue <= 300) {
        description = "Very Unhealthy - Health alert: The risk of health effects is increased for everyone.";
        recommendations = [
            "People with heart or lung disease, older adults, and children should avoid all physical activity outdoors.",
            "Everyone else should avoid prolonged or heavy exertion."
        ];
        position = "76%";
    } else {
        description = "Hazardous - Health warning of emergency conditions: everyone is more likely to be affected.";
        recommendations = [
            "Everyone should avoid all physical activity outdoors.",
            "Remain indoors and keep activity levels low."
        ];
        position = "92%";
    }
    
    // Update the UI with prediction results
    document.getElementById('location-display').textContent = document.getElementById('location').options[document.getElementById('location').selectedIndex].text;
    document.getElementById('aqi-value').textContent = aqiValue;
    document.getElementById('aqi-description').textContent = description;
    document.getElementById('scale-marker').style.left = position;
    
    // Update recommendations
    const recList = document.getElementById('recommendations');
    recList.innerHTML = '';
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recList.appendChild(li);
    });
    
    // Show the result section with animation
    const resultSection = document.getElementById('result-section');
    resultSection.style.display = 'block';
    
    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth' });
}