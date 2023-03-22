import json
import ast
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from .booking import Booking
from django.http import HttpResponse, HttpRequest
from urllib.parse import parse_qs

amadeus = Client(
    client_id='hLMBIHXv892WmW68fznSbddJL0s6uc3a',
    client_secret='CFAdAR5jl3crzHBW', hostname='production'
)

def search_flights(req):
    # Retrieve data from the UI form
    origin = req.GET["originCode"]
    destination = req.GET["destinationCode"]
    departure_date = req.GET["departureDate"]
    return_date = req.GET["returnDate"]
    adults = req.GET["adults"]
    children = req.GET["children"]

    # Prepare url parameters for search
    kwargs = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "children": children,
    }

    # For a round trip, we use AI Trip Purpose Prediction
    # to predict if it is a leisure or business trip
    tripPurpose = ""
    if return_date:
        # Adds the parameter returnDate for the Flight Offers Search API call
        kwargs["returnDate"] = return_date
        kwargs_trip_purpose = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
        }
        try:
            # Calls Trip Purpose Prediction API
            trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(
                **kwargs_trip_purpose
            ).data
            tripPurpose = trip_purpose_response["result"]
        except ResponseError as error:
            messages.add_message(
                req, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
            return render(req, "home.html", {})

    # Perform flight search based on previous inputs
    if origin and destination and departure_date:
        try:
            search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
        except ResponseError as error:
            return render(req, "home.html", {})

        try:
            country = search_flights.result['dictionaries'].get('locations').get(destination).get('countryCode')
            # Get the travel restrictions for the destination
            travel_restrictions = amadeus.duty_of_care.diseases.covid19_report.get(countryCode=country)
            documents = travel_restrictions.data['areaAccessRestriction']['declarationDocuments']['text']
            covid_tests = travel_restrictions.data['areaAccessRestriction']['travelTest']['travelTestConditionsAndRules'][0]['scenarios'][0]['condition']['textualScenario']
        except ResponseError as error:
            messages.add_message(
                req, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
            return render(req, "home.html", {})
        search_flights_returned = []
        response = ""
        for flight in search_flights.data:
            offer = Flight(flight).construct_flights()
            search_flights_returned.append(offer)
            response = zip(search_flights_returned, search_flights.data)

        return render(
            req,
            "flights-category-multi.html",
            {
                "response": response,
                "origin": origin,
                "destination": destination,
                "departureDate": departure_date,
                "returnDate": return_date,
                "tripPurpose": tripPurpose,
                "country": country,
                "documents": documents,
                "covid_tests": covid_tests
            },
        )
    return render(req, "home.html", {})


def book_flight(req, flight):
    # Create a fake traveler profile for booking
    flight_data = json.loads(flight)
    print("flight")
    print("-----------------")
    print("-----------------")
    print("-----------------")
    print("-----------------")
    print(flight_data)
    
    traveler = {
        "id": "1",
        "dateOfBirth": "1982-01-16",
        "name": {"firstName": "JORGE", "lastName": "GONZALES"},
        "gender": "MALE",
        "contact": {
            "emailAddress": "jorge.gonzales833@telefonica.es",
            "phones": [
                {
                    "deviceType": "MOBILE",
                    "countryCallingCode": "34",
                    "number": "480080076",
                }
            ],
        },
        "documents": [
            {
                "documentType": "PASSPORT",
                "birthPlace": "Madrid",
                "issuanceLocation": "Madrid",
                "issuanceDate": "2015-04-14",
                "number": "00000000",
                "expiryDate": "2025-04-14",
                "issuanceCountry": "ES",
                "validityCountry": "ES",
                "nationality": "ES",
                "holder": True,
            }
        ],
    }
    # Use Flight Offers Price to confirm price and availability
    try:
        flight_price_confirmed = amadeus.shopping.flight_offers.pricing.post(
            ast.literal_eval(flight)
        ).data["flightOffers"]
    except ResponseError as error:
        messages.add_message(req, messages.ERROR, error.response.body)
        return render(req, "book_flight.html", {})

    # Use Flight Create Orders to perform the booking
    try:
        order = amadeus.booking.flight_orders.post(
            flight_price_confirmed, traveler
        ).data
    except ResponseError as error:
        messages.add_message(
            req, messages.ERROR, error.response.result["errors"][0]["detail"]
        )
        return render(req, "book_flight.html", {})

    passenger_name_record = []
    booking = Booking(order).construct_booking()
    passenger_name_record.append(booking)

    return render(req, "book_flight.html", {"response": passenger_name_record})

def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]["iataCode"] + ", " + data[i]["name"])
    result = list(dict.fromkeys(result))
    return json.dumps(result)
    
"""
def checkout(req, flight):
    #process flight data to display in checkout page
    query_params = parse_qs(flight.strip('{}'))
    flight_id = query_params['id'][0]
    source = query_params['source'][0]
    departure_time = query_params['itineraries'][0]['segments'][0]['departure']['at']
    arrival_time = query_params['itineraries'][0]['segments'][-1]['arrival']['at']
    price = query_params['price']['total']
    destination = query_params['itineraries'][0]['segments'][-1]['arrival']['iataCode']
    arrival_terminal = query_params['itineraries'][0]['segments'][-1]['arrival']['terminal']
    departure_terminal = query_params['itineraries'][0]['segments'][0]['departure']['terminal']
    adults = query_params['travelers'][0]['adults']
    children = query_params['travelers'][0]['children']
    cabin = query_params['travelClass']


    # Create a fake traveler profile for booking
    traveler = {
        "id": "1",
        "dateOfBirth": "1982-01-16",
        "name": {"firstName": "JORGE", "lastName": "GONZALES"},
        "gender": "MALE",
        "contact": {
            "emailAddress": "   ",
            "phones": [ {"deviceType": "MOBILE", "countryCallingCode": "34", "number": "480080076",},]
        },
        "documents": [
            {
                "documentType": "PASSPORT",
                "birthPlace": "Madrid",
                "issuanceLocation": "Madrid",
                "issuanceDate": "2015-04-14",
                "number": "00000000",
                "expiryDate": "2025-04-14",
                "issuanceCountry": "ES",
                "validityCountry": "ES",
                "nationality": "ES",
                "holder": True,
            }
        ],
    }
 """   