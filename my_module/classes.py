from datetime import datetime

class Flight:
    """
    A class to represent a flight.
    ...

    Attributes
    ----------
    ... [rest of the attributes]
    departure_time : datetime
        The actual departure time of the flight.
    arrival_time : datetime
        The actual arrival time of the flight.
    ...

    Methods
    -------
    ...
    """
    
    def __init__(self, flight_number, airline, departure, departure_code, arrival, arrival_code, departure_time, arrival_time):
        """
        Constructs all the necessary attributes for the Flight object.
        ...
        """
        self.flight_number = flight_number
        self.airline = airline
        self.departure = departure
        self.departure_code = departure_code
        self.arrival = arrival
        self.arrival_code = arrival_code
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def __repr__(self):
        """
        Returns a string representation of the flight.
        """
        return f"{self.airline} flight {self.flight_number} from {self.departure} ({self.departure_code}) to {self.arrival} ({self.arrival_code}) departing at {self.departure_time} arriving at {self.arrival_time}"
