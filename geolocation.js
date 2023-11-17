// Check if the Geolocation API is available in the browser
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(sendPosition);
} else {
    // Geolocation is not available in this browser
    console.log("Geolocation is not supported in your browser.");
}

function sendPosition(position) {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    // Send this data to your Python backend
    fetch('http://localhost:5000/get_coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "lat": lat, "lng": lng }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json(); // Parse the JSON in the response
    })
    .then(data => {
        // Handle the data received from the backend
        console.log('Response from server:', data);
        // You can do more with the data here if needed
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
