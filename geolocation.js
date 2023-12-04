var locationInfo = {
    // origin
    lat: null,
    lng: null,
    // destination
    addr: null
};

// Get user origin
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(updateUserOrigin, handleError);
} else {
    console.log("Geolocation is not supported by your browser.");
}

function handleError(error) {
    console.warn(`ERROR(${error.code}): ${error.message}`);
}


function updateUserOrigin(position) {
    locationInfo.lat = position.coords.latitude;
    locationInfo.lng = position.coords.longitude;
}

// Reads user destination from html text box
function getUserDestination() {
    locationInfo.addr = document.getElementById("user-destination-input").value;

    if (locationInfo.lat != null && locationInfo.lng != null && locationInfo.addr != null) {
        sendLocationInfo();
    }
}

// Sends location information stored in locationInfo
function sendLocationInfo() {
    const{lat, lng, addr} = locationInfo;

    console.log(`lat: ${lat}, lng: ${lng}, address: ${addr}`);

    // Send this data to your Python backend
    if (lat != null && lng != null && addr != null) {
        fetch('http://localhost:5001/get_coordinates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "lat": lat, "lng": lng, "address": addr}),
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
            updateAirportInfo(data);
            // You can do more with the data here if needed
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

function updateAirportInfo(data) {
    if (data.origin_airport && data.des_airport) {
        document.getElementById('origin-airport-name').innerText = data.origin_airport.name;
        document.getElementById('destination-airport-name').innerText = data.des_airport.name;
        document.getElementById('origin-airport-iata').innerText = data.origin_airport.iata_code
        document.getElementById('destination-airport-iata').innerText = data.des_airport.iata_code;


        updateMap(data.origin_airport, data.des_airport); // From mapdata.js
        displayModal(data.origin_airport, data.des_airport, data);
    }
}

function displayModal(orig, dest, data){
    $('#map').on('click', function () {
      $('#modal-origin-airport-name').text(orig.name);
      $('#modal-destination-airport-name').text(dest.name);
      $('#origin-airport-iata').text(`(${orig.iata_code})`);
      $('#destination-airport-iata').text(`(${dest.iata_code})`);
  
      displayAirlineInfo('aa', data.aa);
      displayAirlineInfo('sw', data.sw);
      displayAirlineInfo('sp', data.sp);
      displayAirlineInfo('da', data.da);
      displayAirlineInfo('ua', data.ua);

      $('#airportInfoModal').modal('show');
    });
  }
  
  function displayAirlineInfo(airlineId, info) {
    $(`#${airlineId}-day`).text(info[0]);
    $(`#${airlineId}-duration`).text(info[1]);
  }