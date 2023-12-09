from my_module.functions import fetch_real_time_flights, process_flight_data
import requests_mock
import pytest
from datetime import datetime

def test_fetch_and_process_specific_flight():
    """
    Test fetching and processing data for a specific flight (UA2402).

    This test uses requests_mock to simulate an API response with specific flight data.
    It then checks if the function correctly processes this data.
    """
    mock_response = {
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
                    "scheduled": "2019-12-11T23:30:00+00:00",
                    "estimated": "2019-12-11T23:30:00+00:00",
                    "actual": "2019-12-11T23:34:00+00:00",
                    "runway": "2019-12-11T23:34:00+00:00"
                },
                "arrival": {
                    "airport": "Logan International",
                    "iata": "BOS",
                    "icao": "KBOS",
                    "scheduled": "2019-12-12T07:54:00+00:00",
                    "estimated": "2019-12-12T07:54:00+00:00",
                    "actual": "2019-12-12T07:54:00+00:00",
                    "runway": "2019-12-12T07:54:00+00:00"
                },
                "live": {
                    "is_ground": False
                }
            }
        ]
    }

    with requests_mock.Mocker() as m:
        m.get("http://api.aviationstack.com/v1/flights", json=mock_response)
        
        # Fetch and process the flight data
        flights = fetch_real_time_flights('1b72576d264f229fe85c9a9f8ddda862')
        processed_flights = process_flight_data(flights)

        # Assert that the processed data matches the expected output
        assert len(processed_flights) == 1
        flight = processed_flights[0]
        assert flight.flight_number == "UA2402"
        assert flight.airline == "United Airlines"
        assert flight.departure == "Los Angeles International"
        assert flight.arrival == "Logan International"
        assert flight.departure_time == datetime(2019, 12, 11, 23, 34)
        assert flight.arrival_time == datetime(2019, 12, 12, 7, 54)

def test_fetch_real_time_flights_empty_response():
    """
    Test the behavior of the fetch_real_time_flights function when the API returns an empty response.
    """
    with requests_mock.Mocker() as m:
        m.get("http://api.aviationstack.com/v1/flights", json={"data": []})
        flights = fetch_real_time_flights('test_api_key')
        
        # Assert that the function returns an empty list
        assert flights == []

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
                    "scheduled": "2019-12-11T23:30:00+00:00",
                    "estimated": "2019-12-11T23:30:00+00:00",
                    "actual": "2019-12-11T23:34:00+00:00",
                    "runway": "2019-12-11T23:34:00+00:00"
                },
                "arrival": {
                    "airport": "Logan International",
                    "iata": "BOS",
                    "icao": "KBOS",
                    "scheduled": "2019-12-12T07:54:00+00:00",
                    "estimated": "2019-12-12T07:54:00+00:00",
                    "actual": "2019-12-12T07:54:00+00:00",
                    "runway": "2019-12-12T07:54:00+00:00"
                }
            }
        ]
    }

    processed_data = process_flight_data(sample_api_response["data"])
    
    # Assert that the data is processed correctly
    assert len(processed_data) == 1
    flight = processed_data[0]
    assert flight.flight_number == "UA2402"
    assert flight.airline == "United Airlines"
    assert flight.departure == "Los Angeles International"
    assert flight.arrival == "Logan International"
