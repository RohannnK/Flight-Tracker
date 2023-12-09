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
            flights_in_air.append(flight_info)

    return flights_in_air

def process_flight_data(flight_data):
    """
    Processes raw flight data from the AviationStack API.

    This function takes a list of flight data dictionaries and converts
    them into Flight objects.

    Parameters
    ----------
    flight_data : list of dict
        A list of dictionaries, each representing a flight's data.

    Returns
    -------
    list of Flight
        A list of Flight objects with processed data.
    """
    # List to hold processed Flight objects
    processed_flights = []

    # Processing each flight in the data
    for flight in flight_data:
        # Extracting relevant information
        flight_number = flight['flight_number']
        airline = flight['airline']
        departure_airport = flight['departure']
        departure_code = flight['departure_code']
        arrival_airport = flight['arrival']
        arrival_code = flight['arrival_code']

        # Creating a Flight object
        processed_flight = Flight(flight_number, airline, departure_airport, departure_code, arrival_airport, arrival_code)
        
        # Adding the Flight object to the list
        processed_flights.append(processed_flight)

    return processed_flights
