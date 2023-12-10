import requests
from .classes import Flight  
from datetime import datetime

def fetch_real_time_flights(api_key, limit=100, offset=0):
    """
    Fetch real-time flight data from the AviationStack API.

    Parameters
    ----------
    api_key : str
        The API key required to authenticate with the AviationStack API.
    limit : int, optional
        The number of results to return per request (default is 100).
    offset : int, optional
        The offset for pagination (default is 0).

    Returns
    -------
    list of dict
        A list of dictionaries, each containing information about a flight.
    """
    params = {
        'access_key': api_key,
        'limit': limit,
        'offset': offset
    }
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
    api_response = api_result.json()
    print(api_response)
    flights_in_air = []

    for flight in api_response.get('data', []):
        # Check if 'live' data is available and if the flight is not on the ground
        live_data = flight.get('live')
        if live_data and not live_data.get('is_ground', True):
            flight_info = {
                'airline': flight.get('airline', {}).get('name'),
                'flight_number': flight.get('flight', {}).get('iata'),
                'departure_airport': flight.get('departure', {}).get('airport'),
                'departure_iata': flight.get('departure', {}).get('iata'),
                'arrival_airport': flight.get('arrival', {}).get('airport'),
                'arrival_iata': flight.get('arrival', {}).get('iata')
            }
            flights_in_air.append(flight_info)
    print("Final Flights in Air:", flights_in_air)
    return flights_in_air


def process_flight_data(flight_data):
    """
    Processes raw flight data into Flight objects.

    Args:
        flight_data (list): A list of raw flight data.

    Returns:
        list: A list of Flight objects with processed data.
    """
    processed_flights = []
    
    for flight_info in flight_data:
        flight = flight_info.get("flight", {})
        airline = flight_info.get("airline", flight_info.get("airline_name", {}))  # Handle both cases
        departure = flight_info.get("departure", {})
        arrival = flight_info.get("arrival", {})
        
        processed_flight = Flight(
            flight_number=flight.get("number", ""),
            airline=airline.get("name", ""),
            departure_airport=departure.get("airport", ""),
            departure_iata=departure.get("iata", ""),
            arrival_airport=arrival.get("airport", ""),
            arrival_iata=arrival.get("iata", "")
        )
        processed_flights.append(processed_flight)
    
    return processed_flights
