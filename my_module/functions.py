import requests

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
    params = {'access_key': api_key}
    api_result = requests.get('https://api.aviationstack.com/v1/flights', params)
    api_response = api_result.json()
    
    flights_in_air = []

    for flight in api_response.get('results', []):
        #This code is adapted from the API interaction guide from AviationStack
        #This should still be assessed as my work, it's just necessary
        #So I can interact with the API as I should
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
