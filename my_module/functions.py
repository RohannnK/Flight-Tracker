import requests
from .classes import Flight  # Import the Flight class from classes module

def fetch_real_time_flights(api_key):
    """
    Fetch real-time flight data from the AviationStack API.

    This function sends a request to the AviationStack API to retrieve
    information about flights that are currently in the air.

    Parameters
    ----------
    api_key : str
        The API key required to authenticate with the AviationStack API.

    Returns
    -------
    list of dict
        A list of dictionaries, each containing information about a flight.
        Each dictionary includes the airline name, flight number, departure
        and arrival airports, and their respective IATA codes.

    Raises
    ------
    requests.exceptions.RequestException
        If the request to the AviationStack API fails.

    Examples
    --------
    >>> flights = fetch_real_time_flights('your_api_key_here')
    >>> for flight in flights:
    ...     print(flight)
    """
    # Parameters for the API request
    params = {'access_key': api_key}
    
    # Making the API request
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
    api_response = api_result.json()
    print("API Response:", api_response)

    # List to hold flight information
    flights_in_air = []

    # Processing each flight in the response
    for flight in api_response.get('results', []):
        if not flight['live']['is_ground']:
            flight_info = {
                'airline': flight['airline']['name'],
                'flight_number': flight['flight']['iata'],
                'departure': flight['departure']['airport'],
                'departure_code': flight['departure']['iata'],
                'arrival': flight['arrival']['airport'],
                'arrival_code': flight['arrival']['iata']
            }
            print("Flight Info:", flight_info)
            flights_in_air.append(flight_info)
    print("Flights in Air:", flights_in_air)
    return flights_in_air

def process_flight_data(flight_data):
    processed_flights = []

    for flight in flight_data:
        # Create a Flight object with dummy values for testing
        test_flight = Flight("Test123", "TestAirline", "TestDeparture", "TD", "TestArrival", "TA")
        processed_flights.append(test_flight)

    return processed_flights
