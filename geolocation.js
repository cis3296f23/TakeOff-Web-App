/**
 * Object declaration of locationInfo that has latitude & longitude for origin location as well as address for destination location
 */

var locationInfo = {
    // origin
    lat: null,
    lng: null,
    // destination
    addr: null
};

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(updateUserOrigin, handleError);
} else {
    console.log("Geolocation is not supported by your browser.");
}

/**
 * Handles any errors
 * @param {*} error Error
 */

function handleError(error) {
    console.warn(`ERROR(${error.code}): ${error.message}`);
}

/**
 * Updates user's origin using latitude & longitude from the locationInfo
 * @param {*} position Position of user
 */

function updateUserOrigin(position) {
    locationInfo.lat = position.coords.latitude;
    locationInfo.lng = position.coords.longitude;
}


/**
 * Reads user destination from HTML text box
 */

function getUserDestination() {
    locationInfo.addr = document.getElementById("user-destination-input").value;

    if (locationInfo.lat != null && locationInfo.lng != null && locationInfo.addr != null) {
        sendLocationInfo();
    }
}

/**
 * Sends location information stored in locationInfo to Python backend
 */

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
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

/**
 * Update airport information based off 
 * @param {*} data Airport data
 */

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

/**
 * Function to display modal for pop-up functionality to show all airport & airline information
 * @param {*} orig Origin airport
 * @param {*} dest Destination airport
 * @param {*} data Airline data
 */

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

/**
 * Displaying airline information including day & duration 
 * @param {*} airlineId Airline ID Ex: "sp" is Spirit Airlines
 * @param {*} info Airline information
 */

  function displayAirlineInfo(airlineId, info) {
    $(`#${airlineId}-day`).text(info[0]);
    $(`#${airlineId}-duration`).text(info[1]);
}