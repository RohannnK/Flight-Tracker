import requests
from .classes import Flight  
from datetime import datetime
import pandas as pd

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
    Processes raw flight data from AviationStack API into Flight objects using pandas.

    Parameters
    ----------
    flight_data_list : list
        A list of dictionaries, each a flight record from the AviationStack API.

    Returns
    -------
    list
        A list of Flight objects with processed data.
    """

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(flight_data)

    # Normalize the nested dictionaries into separate columns
    df_flight = pd.json_normalize(df['flight']).add_prefix('flight_')
    df_airline = pd.json_normalize(df['airline']).add_prefix('airline_')
    df_departure = pd.json_normalize(df['departure']).add_prefix('departure_')
    df_arrival = pd.json_normalize(df['arrival']).add_prefix('arrival_')

    # Join the normalized data back into the main DataFrame
    df = df.join([df_flight, df_airline, df_departure, df_arrival])

    # Drop the original nested structure columns
    df = df.drop(columns=['flight', 'airline', 'departure', 'arrival'])

    # Convert the datetime strings to datetime objects
    df['departure_actual'] = pd.to_datetime(df['departure_actual'], errors='coerce')
    df['arrival_actual'] = pd.to_datetime(df['arrival_actual'], errors='coerce')

    # Drop any rows where the required data is missing
    required_columns = [
        'flight_iata', 'airline_name', 'departure_airport', 'departure_iata', 
        'arrival_airport', 'arrival_iata', 'departure_actual', 'arrival_actual'
    ]
    df = df.dropna(subset=required_columns)

    # Create Flight objects from the DataFrame rows
    processed_flights = [
        Flight(
            flight_number=row['flight_iata'],
            airline=row['airline_name'],
            departure=row['departure_airport'],
            departure_code=row['departure_iata'],
            arrival=row['arrival_airport'],
            arrival_code=row['arrival_iata'],
            departure_time=row['departure_actual'],
            arrival_time=row['arrival_actual']
        )
        for _, row in df.iterrows()
    ]

    return processed_flights