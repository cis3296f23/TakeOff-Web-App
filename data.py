""" Description: Gets all data needed for the backend including user's location coordinates, origin & destination airport information, airlines information, and route information. 
"""

# import pydoc
import json
import geocoder
import requests
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes or specify origins with CORS(app, origins="*") for all origins


# Function to find the nearest popular airport given a latitude and longitude
def origin(lat, lng):

    """ Description: Gets the airports from user's nearby location using their latitude & longitude with Airlabs API
    Return: 1 airport filtered by popularity

    Parameters: 
        lat - latitude
        lng - longitude
    """

     # Parameters for the API request: API key, latitude, longitude, and search distance
    origin_params = {
        'api_key': 'afc3037c-40d6-4090-b7ff-d0c9ea928454',
        'lat': lat,
        'lng': lng,
        'distance': '50' # Distance in kilometers
    }
     # API endpoint URL for finding nearby airports
    origin_url = 'https://airlabs.co/api/v9/nearby'
    # Making a GET request to the API
    origin_response = requests.get(origin_url, params=origin_params)
    # Check if the API request was successful
    if origin_response.status_code == 200:
         # Parse the JSON response
        origin_data = origin_response.json()
        # Extract the list of airports within the specified distance
        airports = origin_data.get('response', {}).get('airports', [])
        # Default to the first airport in the list
        origin_airport = airports[0]
        # Iterate through the list of airports
        for airport in airports:
            # Check if the airport has an IATA code
            if (airport.get("iata_code") != None):
                # Compare the popularity of the airports, select the more popular one
                if origin_airport.get("popularity") < airport.get("popularity"):
                    origin_airport = airport
    else:
        print("API request failed with status code:", origin_response.status_code)
    # Return the most popular airport found
    return origin_airport


# Function to find the nearest popular destination airport given a latitude and longitude
def des(lat, lng):

    """ Description: Gets the nearest popular destination airports using AirLabs API given the latitude & longitude

    Parameters: 
        lat - latitude
        lng - longitude
    """

    # Parameters for the API request: API key, latitude, longitude, and search distance
    des_params = {
        'api_key': 'afc3037c-40d6-4090-b7ff-d0c9ea928454',
        'lat': lat,
        'lng': lng,
        'distance': '75'  # Distance in kilometers
    }

    # API endpoint URL for finding nearby airports
    des_url = 'https://airlabs.co/api/v9/nearby'

    # Making a GET request to the API
    des_response = requests.get(des_url, params=des_params)

    # Check if the API request was successful
    if des_response.status_code == 200:
        # Initialize an empty list to hold destination airports
        des_airports = []

        # Parse the JSON response from the API
        des_data = des_response.json()

        # Extract the list of airports within the specified distance
        airports = des_data.get('response', {}).get('airports', [])

        # Default to the first airport in the list
        des_airport = airports[0]

        # Iterate through the list of airports
        for airport in airports:
            # Check if the airport has an IATA code
            if airport.get("iata_code") is not None:
                # Compare the popularity of the airports, select the more popular one
                if des_airport.get("popularity") < airport.get("popularity"):
                    des_airport = airport
    else:
        # Print an error message if the API request failed
        print("API request failed with status code:", des_response.status_code)

    # Return the most popular destination airport found
    return des_airport


# Parameters for the API request: API key and country code
airline_params = {
    'api_key': 'afc3037c-40d6-4090-b7ff-d0c9ea928454',
    'country_code': 'US'
}

# Function to get data of specific airlines
def get_airlines():

    """ Description: Gets specific airline data from the 5 most common airlines used in the US using Airlabs API
    Return: The 5 airline names with their IATA codes
    """

    # Initial dictionary to store airline names and their respective IATA and ICAO codes
    airlines = {
        # List of 5 most common airlines used in the US
        'names': ["American Airlines", "Southwest Airlines", "Spirit Airlines", "Delta Air Lines", "United Airlines"],
        'iata_codes': [],  # Empty list to store IATA codes
        'icao_codes': []   # Empty list to store ICAO codes
    }

    # Making a GET request to the API
    airline_response = requests.get('https://airlabs.co/api/v9/airlines', params=airline_params)

    # Check if the API request was successful
    if airline_response.status_code == 200:
        # Parse the JSON response
        airline_data = airline_response.json().get('response', {})

        # Iterate through the data to find matching airlines
        for data in airline_data:
            # Check if the airline data has both IATA and ICAO codes and is in the list of target airlines
            if data['iata_code'] is not None and data['icao_code'] is not None and data['name'] in airlines['names']:
                # Append the IATA and ICAO codes to the respective lists
                airlines['iata_codes'].append(data['iata_code'])
                airlines['icao_codes'].append(data['icao_code'])
    else:
        # Print an error message if the API request failed
        print("API request failed with status code:", airline_response.status_code)

    # Return the dictionary containing the airlines' names and codes
    return airlines


# Function to get flight routes for given origin and destination airports and a list of airlines
def get_routes(origin_airport, des_airport, airlines):

    """ Description: Gets flight route information based off origin airport, destination airport, & list of airlines using AirLabs API
    Return: Each routes' day of flight & duration of flight in minutes

    Parameters: 
        origin_airport - origin airport
        des_airport - destination airport
        airlines - airlines
    """
    # Initialize a dictionary to store the flight times for each airline
    times = {}

    # Loop through each of the first 5 airlines in the list
    for i in range(5):
        # Parameters for the API request including airport and airline codes
        route_params = {
            'api_key': 'afc3037c-40d6-4090-b7ff-d0c9ea928454',
            'dep_iata': origin_airport.get('iata_code'),    # Departure airport IATA code
            'dep_icao': origin_airport.get('icao_code'),    # Departure airport ICAO code
            'arr_iata': des_airport.get("iata_code"),       # Arrival airport IATA code
            'arr_icao': des_airport.get("icao_code"),       # Arrival airport ICAO code
            'airline_icao': airlines['icao_codes'][i],      # Airline ICAO code
            'airline_iata': airlines['iata_codes'][i]       # Airline IATA code
        }

        # Making a GET request to the API
        route_response = requests.get('https://airlabs.co/api/v9/routes', params=route_params)

        # Check if the API request was successful
        if route_response.status_code == 200:
            # Parse the JSON response
            route_data = route_response.json().get('response', {})

            # Check if the route data is available
            if route_data:
                # Initialize the shortest duration and day of flight
                shortest = route_data[0]['duration']
                day = ""

                # Iterate through each route in the data
                for data in route_data:
                    # Compare and find the shortest duration
                    if data['duration'] < shortest:
                        shortest = data['duration']
                        day = data['days'][0].upper()  # Get the day of the shortest flight in uppercase

                # Handle cases where flight day or duration data is missing
                if day == "":
                    day = "Flight day is not available. Please check again later."
                if shortest == "":
                    shortest = "There are no available flights to this destination."

                # Store the flight day and duration in the times dictionary for the airline
                times[airlines['names'][i]] = [day, str(shortest) + " minutes"]
            else:
                # Store default values in case of no route data
                times[airlines['names'][i]] = ["Flight day is not available. Please check again later.", "There are no available flights to this destination."]
        else:
            # Print an error message if the API request failed
            print("API request failed with status code:", route_response.status_code)

    # Return the dictionary containing flight times for each airline
    return times

# Route to handle the POST request to '/get_coordinates'
@app.route('/get_coordinates', methods=['POST'])
def get_coordinates():

    """ Description: Gets user's current location coordinates to determine the destination airport & get airlines to r
    Return: Jsonify objects of information including origin & destination airport, flight information from each of the airlines with a message saying that data has been processed 
    """

    # Retrieve and parse the JSON data sent in the POST request
    data = request.get_json()
    lat = data['lat']
    lng = data['lng']

    # Get the nearest popular origin airport using the latitude and longitude
    origin_airport = origin(lat, lng)

    # Use geocoder to find the latitude and longitude for the provided address
    location = geocoder.osm(data['address'])
    lat, long = location.lat, location.lng

    # Get the nearest popular destination airport using the latitude and longitude from geocoder
    des_airport = des(lat, long)

    # Retrieve information about airlines
    airlines = get_airlines()

    # Get route information for the origin and destination airports for the specified airlines
    info = get_routes(origin_airport, des_airport, airlines)

    # Return the data as a JSON response
    return jsonify({
        'origin_airport': origin_airport,  # Information about the origin airport
        'des_airport': des_airport,        # Information about the destination airport
        'aa': info.get('American Airlines', {}),  # Route info for American Airlines
        'sw': info.get('Southwest Airlines', {}),  # Route info for Southwest Airlines
        'sp': info.get('Spirit Airlines', {}),    # Route info for Spirit Airlines
        'da': info.get('Delta Air Lines', {}),    # Route info for Delta Air Lines
        'ua': info.get('United Airlines', {}),    # Route info for United Airlines
        'message': 'Data processed'  # Confirmation message
    })

# Run the Flask app when this script is executed
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run the app in debug mode on port 5001
    # pydoc.writedoc('data')