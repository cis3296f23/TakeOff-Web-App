""" Description: Gets all data needed for the backend including user's location coordinates, origin & destination airport information, airlines information, and route information. 
"""

import json
import geocoder
import requests
import pydoc
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes or specify origins with CORS(app, origins="*") for all origins

# first get airports nearby your location
def origin(lat, lng):
    
    """ Description: Gets the airports from user's nearby location using their latitude & longitude with Airlabs API
    Return: 1 airport filtered by popularity

    Parameters: 
        lat - latitude
        lng - longitude
    """

    origin_params = {
        'api_key': 'bb693f91-a910-449b-ad69-b9699f7991db',
        'lat': lat,
        'lng': lng,
        'distance': '50'
    }
    origin_url = 'https://airlabs.co/api/v9/nearby'
    origin_response = requests.get(origin_url, params=origin_params)
    if origin_response.status_code == 200:
        origin_data = origin_response.json()
        airports = origin_data.get('response', {}).get('airports', [])
        origin_airport = airports[0]
        for airport in airports:
            if (airport.get("iata_code") != None):
                if origin_airport.get("popularity") < airport.get("popularity"):
                    origin_airport = airport
    else:
        print("API request failed with status code:", origin_response.status_code)
    return origin_airport


# get destination airports
def des(lat, lng):
    
    """ Description: Gets the destination airports using AirLabs API by popularity of airport

    Parameters: 
        lat - latitude
        lng - longitude
    """

    des_params = {
        'api_key': 'bb693f91-a910-449b-ad69-b9699f7991db',
        'lat': lat,
        'lng': lng,
        'distance': '50'
    }
    des_url = 'https://airlabs.co/api/v9/nearby'
    des_response = requests.get(des_url, params=des_params)

    if des_response.status_code == 200:
        des_airports = []
        des_data = des_response.json()
        airports = des_data.get('response', {}).get('airports', [])
        des_airport = airports[0]
        for airport in airports:
            if (airport.get("iata_code") != None):
                if des_airport.get("popularity") < airport.get("popularity"):
                    des_airport = airport
    else:
        print("API request failed with status code:", des_response.status_code)
    return des_airport


airline_params = {
    'api_key': 'bb693f91-a910-449b-ad69-b9699f7991db',
    'country_code': 'US'
}


def get_airlines():
    
    """ Description: Gets 5 most common airlines used in the US and their IATA codes using Airlabs API
    Return: The 5 airlines with their IATA codes
    """

    airlines = {
         # 5 most common airlines used in US
        'names': ["American Airlines", "Southwest Airlines", "Spirit Airlines", "Delta Air Lines", "United Airlines"],
        'iata_codes': [],
        'icao_codes': []
    }
   
    airline_response = requests.get('https://airlabs.co/api/v9/airlines', params=airline_params)
    if airline_response.status_code == 200:
        airline_data = airline_response.json()
        airline_data = airline_data.get('response', {})
        for data in airline_data:
            if data['iata_code'] != None and data['icao_code'] != None and data['name'] in airlines['names']:
                airlines['iata_codes'].append(data['iata_code'])
                airlines['icao_codes'].append(data['icao_code'])
    else:
        print("API request failed with status code:", airline_response.status_code)
    return airlines


def get_routes(origin_airport, des_airport, airlines):
    
    """ Description: Gets flight route information based off origin airport, destination airport, & airlines using AirLabs API
    Return: Each routes' day of flight & duration of flight in minute

    Parameters: 
        origin_airport - origin airport
        des_airport - destination airport
        airlines - airlines
    """

    times = {}
    
    for i in range(5):
        route_params = {
            'api_key': 'bb693f91-a910-449b-ad69-b9699f7991db',
            'dep_iata': origin_airport.get('iata_code'),
            'dep_icao': origin_airport.get('icao_code'),
            'arr_iata': des_airport.get("iata_code"),
            'arr_icao': des_airport.get("icao_code"),
            'airline_icao': airlines['icao_codes'][i],
            'airline_iata': airlines['iata_codes'][i]
        }
        route_response = requests.get('https://airlabs.co/api/v9/routes', params=route_params)
        if route_response.status_code == 200:
            route_data = route_response.json()
            route_data = route_data.get('response', {})
            if route_data:
                shortest = route_data[0]['duration']
                day = ""
                for data in route_data:
                    if data['duration'] < shortest:
                        shortest = data['duration']
                        day = data['days'][0].upper()
                if day == "":
                    day = "Flight day is not available. Please check again later."
                if shortest == "":
                    shortest = "There are no available flights to this destination."
                times[airlines['names'][i]] = [day, str(shortest) + " minutes"]
            else:
                 times[airlines['names'][i]] = ["Flight day is not available. Please check again later.", "There are no available flights to this destination."]
        else:
            print("API request failed with status code:", route_response.status_code)
    return times
    
@app.route('/get_coordinates', methods=['POST'])
def get_coordinates():

    """ Description: Gets user's current location coordinates to determine the destination airport & get airlines to r
    Return: Jsonify objects of information including origin & destination airport, flight information from each of the airlines with a message saying that data has been processed 
    """

    data = request.get_json()
    
    lat = data['lat']
    lng = data['lng']
    origin_airport = origin(lat, lng)
    location = geocoder.osm(data['address'])
    lat, long = location.lat, location.lng
    des_airport = des(lat, long)
    airlines = get_airlines()
    info = get_routes(origin_airport, des_airport, airlines)
    return jsonify({
        'origin_airport': origin_airport,
        'des_airport': des_airport,
        'aa': info.get('American Airlines', {}),
        'sw': info.get('Southwest Airlines', {}),
        'sp': info.get('Spirit Airlines', {}),
        'da': info.get('Delta Air Lines', {}),
        'ua': info.get('United Airlines', {}),
        'message': 'Data processed'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
pydoc.writedoc('data')