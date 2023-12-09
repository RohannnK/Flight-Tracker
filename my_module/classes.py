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
    arrival : str
        The arrival airport of the flight.

    Methods
    -------
    __str__()
        Returns a string representation of the flight, including the airline,
        flight number, departure, and arrival airports.
    """

    def __init__(self, flight_number, airline, departure, arrival):
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
            arrival : str
                The arrival airport of the flight.
        """
        self.flight_number = flight_number
        self.airline = airline
        self.departure = departure
        self.arrival = arrival

    def __str__(self):
        """
        Returns a string representation of the flight.

        This method returns a string that includes the airline, flight number,
        and the departure and arrival airports of the flight.

        Returns
        -------
        str
            A string representation of the flight.
        """
        return f"{self.airline} flight {self.flight_number} from {self.departure} to {self.arrival}"