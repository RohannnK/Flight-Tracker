import sys
sys.path.append('/Users/rohankaman/Documents/GitHub/Flight-Tracker')

from my_module.functions import fetch_real_time_flights, process_flight_data
import requests_mock
from datetime import datetime

def test_fetch_and_process_specific_flight():
    """
    Test fetching and processing data for a specific flight.
    """
    mock_response = [
        {
            "flight": {
                "iata": "UA2402",
                "icao": "UAL2402",
                "number": "2402"
            },
            "airline": {
                "name": "United Airlines",
                "iata": "UA",
                "icao": "UAL"
            },
            "departure": {
                "airport": "Los Angeles International",
                "iata": "LAX",
                "icao": "KLAX",
                "scheduled": "2019-12-11T23:30:00+00:00"
            },
            "arrival": {
                "airport": "Logan International",
                "iata": "BOS",
                "icao": "KBOS",
                "scheduled": "2019-12-12T07:54:00+00:00"
            },
            "live": {
                "is_ground": False
            }
        }
    ]

    with requests_mock.Mocker() as m:
        m.get("http://api.aviationstack.com/v1/flights", json=mock_response)
        flights_data = fetch_real_time_flights('dummy_api_key')
        processed_flights = process_flight_data(flights_data)

        assert len(processed_flights) == 1
        flight = processed_flights[0]
        assert flight.flight_number == "UA2402"
        assert flight.airline == "United Airlines"
        assert flight.departure == "Los Angeles International"
        assert flight.arrival == "Logan International"
        assert flight.departure_time == datetime.fromisoformat("2019-12-11T23:30:00+00:00")
        assert flight.arrival_time == datetime.fromisoformat("2019-12-12T07:54:00+00:00")

def test_fetch_real_time_flights_empty_response():
    """
    Test the behavior of the fetch_real_time_flights function when the API returns an empty response.
    """
    with requests_mock.Mocker() as m:
        m.get("http://api.aviationstack.com/v1/flights", json=[])
        flights_data = fetch_real_time_flights('dummy_api_key')
        assert flights_data == []

def test_process_flight_data_extraction():
    """
    Test if the process_flight_data function correctly extracts and formats the necessary information.
    """
    sample_api_response = {
        "data": [
            {
                "flight": {
                    "iata": "UA2402",
                    "icao": "UAL2402",
                    "number": "2402"
                },
                "airline": {
                    "name": "United Airlines",
                    "iata": "UA",
                    "icao": "UAL"
                },
                "departure": {
                    "airport": "Los Angeles International",
                    "iata": "LAX",
                    "icao": "KLAX",
                    "scheduled": "2019-12-11T23:30:00+00:00"
                },
                "arrival": {
                    "airport": "Logan International",
                    "iata": "BOS",
                    "icao": "KBOS",
                    "scheduled": "2019-12-12T07:54:00+00:00"
                }
            }
        ]
    }

    processed_data = process_flight_data(sample_api_response["data"])
    assert len(processed_data) == 1
    flight = processed_data[0]
    assert flight.flight_number == "UA2402"
    assert flight.airline == "United Airlines"
    assert flight.departure == "Los Angeles International"
    assert flight.arrival == "Logan International"

def test_process_flight_data_datetime_conversion():
    """
    Test if the process_flight_data function correctly converts datetime strings to datetime objects.
    """
    sample_api_response = {
        "data": [
            {
                "flight": {
                    "iata": "AA123",
                    "icao": "AAL123",
                    "number": "123"
                },
                "airline": {
                    "name": "American Airlines",
                    "iata": "AA",
                    "icao": "AAL"
                },
                "departure": {
                    "airport": "JFK Airport",
                    "iata": "JFK",
                    "icao": "KJFK",
                    "scheduled": "2023-12-09T12:30:00+00:00"
                },
                "arrival": {
                    "airport": "Los Angeles International",
                    "iata": "LAX",
                    "icao": "KLAX",
                    "scheduled": "2023-12-09T17:45:00+00:00"
                }
            }
        ]
    }

    processed_data = process_flight_data(sample_api_response["data"])
    assert len(processed_data) == 1
    flight = processed_data[0]
    assert flight.departure_time == datetime.fromisoformat("2023-12-09T12:30:00+00:00")
    assert flight.arrival_time == datetime.fromisoformat("2023-12-09T17:45:00+00:00")
