import requests
from datetime import datetime
from .classes import Flight

def fetch_real_time_flights(api_key, limit=100, offset=0):
    """
    Fetches real-time flight data from the AviationStack API.

    Parameters
    ----------
    api_key : str
        Your API access key for the AviationStack API.
    limit : int, optional
        The maximum number of flight records to fetch (default is 100).
    offset : int, optional
        The pagination offset to start fetching flight records (default is 0).

    Returns
    -------
    list
        A list of dictionaries, each representing a flight record as returned by the API.

    Raises
    ------
    HTTPError
        An error occurs from the HTTP request.
    """
    params = {
        'access_key': api_key,
        'limit': limit,
        'offset': offset
    }
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params=params)
    api_result.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    api_response = api_result.json()

    # Determine if the API response is a list and return it, otherwise return the 'data' part of the response.
    return api_response if isinstance(api_response, list) else api_response.get('data', [])

def process_flight_data(flights_data):
    """
    Processes a list of flight data dictionaries into a list of Flight objects.

    Parameters
    ----------
    flights_data : list
        A list of dictionaries where each dictionary contains data for a single flight.

    Returns
    -------
    list
        A list of Flight objects with processed data.

    Notes
    -----
    Each Flight object in the returned list is initialized with the data extracted from
    the input dictionaries, where each dictionary corresponds to a flight record.
    """
    processed_flights = []

    for flight_info in flights_data:
        # Extract and convert necessary information from each flight record.

        flight_number = flight_info["flight"]["iata"]

        airline = flight_info["airline"]["name"]

        departure_airport = flight_info["departure"]["airport"]

        departure_iata = flight_info["departure"]["iata"]

        arrival_airport = flight_info["arrival"]["airport"]

        arrival_iata = flight_info["arrival"]["iata"]

        departure_time = datetime.fromisoformat(flight_info["departure"]["scheduled"])

        arrival_time = datetime.fromisoformat(flight_info["arrival"]["scheduled"])

        # Initialize a Flight object with the extracted information and add it to the list.
        processed_flight = Flight(

            flight_number=flight_number,

            airline=airline,

            departure=departure_airport,

            departure_code=departure_iata,

            arrival=arrival_airport,

            arrival_code=arrival_iata,

            departure_time=departure_time,

            arrival_time=arrival_time
        )
        processed_flights.append(processed_flight)

    return processed_flights
