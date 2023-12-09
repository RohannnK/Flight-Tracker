import requests
from .classes import Flight  

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

    return flights_in_air


def process_flight_data(flight_data):
    """
    Processes raw flight data into Flight objects.

    Parameters
    ----------
    flight_data : list of dict
        A list of dictionaries, each representing a flight's data.

    Returns
    -------
    list of Flight
        A list of Flight objects with processed data.
    """
    processed_flights = []

    for flight in flight_data:
        processed_flight = Flight(
            flight_number=flight['flight_number'],
            airline=flight['airline'],
            departure_airport=flight['departure_airport'],
            departure_iata=flight['departure_iata'],
            arrival_airport=flight['arrival_airport'],
            arrival_iata=flight['arrival_iata']
        )
        processed_flights.append(processed_flight)

    return processed_flights
