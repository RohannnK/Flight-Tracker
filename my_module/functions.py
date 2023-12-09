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
    print(api_response)
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
    Processes raw flight data into Flight objects.

    This function takes a list of flight data dictionaries, each representing
    a flight's data, and converts them into Flight objects. It ensures that
    each flight record has all the necessary information before creating a
    Flight object. If any information is missing, it skips that record and
    prints a message.

    Parameters
    ----------
    flight_data : list of dict
        A list of dictionaries, each representing a flight's data.

    Returns
    -------
    list of Flight
        A list of Flight objects with processed data.

    Notes
    -----
    The function uses a try-except block to catch any unexpected errors during
    the processing of each flight record.
    """

    # List to hold processed Flight objects
    processed_flights = []

    # Processing each flight in the data
    for flight in flight_data:
        try:
            # Safely extracting flight details
            flight_number = flight.get('flight_number')
            airline = flight.get('airline')
            departure_airport = flight.get('departure')
            departure_code = flight.get('departure_code')
            arrival_airport = flight.get('arrival')
            arrival_code = flight.get('arrival_code')

            # Check if all required data is present
            if all([flight_number, airline, departure_airport, departure_code, arrival_airport, arrival_code]):
                # Creating a Flight object
                processed_flight = Flight(flight_number, airline, departure_airport, departure_code, arrival_airport, arrival_code)
                processed_flights.append(processed_flight)
            else:
                # Print a message if any data is missing
                print("Missing data in flight record:", flight)
        except Exception as e:
            # Print any errors encountered during processing
            print("Error processing flight data:", e)

    return processed_flights
