# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BookingDetails:
    def __init__(
        self,
        destination: str = None,
        origin: str = None,
        travel_departure_date: str = None,
        travel_return_date: str = None,
        budget: str = None #,
        #unsupported_airports=None
        
    ):
        #if unsupported_airports is None:
        #    unsupported_airports = []
        self.destination = destination
        self.origin = origin
        self.travel_departure_date = travel_departure_date,
        self.travel_return_date = travel_return_date
        self.budget = budget 
        #self.unsupported_airports = unsupported_airports
