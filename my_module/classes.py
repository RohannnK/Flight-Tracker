class Flight:
    """
    A class to represent a flight.

    Attributes
    ----------
    flight_number : str
        The flight number of the flight.
    airline : str
        The airline operating the flight.
    departure : str
        The departure airport of the flight.
    departure_code : str
        The IATA code of the departure airport.
    arrival : str
        The arrival airport of the flight.
    arrival_code : str
        The IATA code of the arrival airport.

    Methods
    -------
    __str__()
        Returns a string representation of the flight, including the airline,
        flight number, departure, and arrival airports.
    """

    def __init__(self, flight_number, airline, departure, departure_code, arrival, arrival_code):
        """
        Constructs all the necessary attributes for the Flight object.

        Parameters
        ----------
            flight_number : str
                The flight number of the flight.
            airline : str
                The airline operating the flight.
            departure : str
                The departure airport of the flight.
            departure_code : str
                The IATA code of the departure airport.
            arrival : str
                The arrival airport of the flight.
            arrival_code : str
                The IATA code of the arrival airport.
        """
        self.flight_number = flight_number
        self.airline = airline
        self.departure = departure
        self.departure_code = departure_code
        self.arrival = arrival
        self.arrival_code = arrival_code

    def __str__(self):
        """
        Returns a string representation of the flight.

        This method returns a string that includes the airline, flight number,
        departure and arrival airports, and their IATA codes.

        Returns
        -------
        str
            A string representation of the flight.
        """
        return f"{self.airline} flight {self.flight_number} from {self.departure} ({self.departure_code}) to {self.arrival} ({self.arrival_code})"
