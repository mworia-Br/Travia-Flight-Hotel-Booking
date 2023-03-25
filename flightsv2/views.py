import json
import ast
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from .booking import Booking
from .models import FlightTmp
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from flight.models import CartItem, SearchedRoute

amadeus = Client(
    client_id='hLMBIHXv892WmW68fznSbddJL0s6uc3a',
    client_secret='CFAdAR5jl3crzHBW', hostname='production'
)

@login_required(login_url='login')
def search_flights(req):
    # Retrieve data from the UI form
    origin = req.GET["originCode"]
    destination = req.GET["destinationCode"]
    departure_date = req.GET["departureDate"]
    return_date = req.GET["returnDate"]
    adults = req.GET["adults"]
    children = req.GET["children"]
    short_Origin = req.GET["shortOrigin"]
    short_Destination = req.GET["shortDestination"]
    long_Origin = req.GET["longOrigin"]
    long_Destination = req.GET["longDestination"]
    travellers = int(adults) + int(children)
    currency = 'USD'
    owner=req.user

    # Create a new SearchedRoute object and save it to the database
    route = SearchedRoute.objects.create(
        origin=origin, 
        destination=destination, 
        departure_date=departure_date,
        adults_count=adults,
        children_count=children
    )

    # Prepare url parameters for search
    kwargs = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "children": children,
        #"currency": currency
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
            "adults": adults,
            "children": children,
            #"currency": currency
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
            documents = travel_restrictions.data['areaAccessRestriction']['declarationDocuments'].get('text', None)
            covid_tests = travel_restrictions.data['areaAccessRestriction']['travelTest']['travelTestConditionsAndRules'][0]['scenarios'][0]['condition']['textualScenario']
        except ResponseError as error:
            messages.add_message(
                req, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
            return render(req, "home.html", {})
        search_flights_returned = []
        response = ""
        for flight in search_flights.data:
            offer = Flight(flight, origin, destination, travellers, owner, short_Origin, short_Destination, long_Destination, long_Origin).construct_flights()
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

@login_required(login_url="/login")
def checkoutHandle(req):
    # Get the variables from the query parameters
    # Extract flight variables from query parameters
    firstFlightDepartureAirport = req.GET.get('0firstFlightDepartureAirport', None)
    firstFlightDepartureDate = req.GET.get('0firstFlightDepartureDate', None)
    firstFlightAirlineLogo = req.GET.get('0firstFlightAirlineLogo', None)
    firstFlightAirline = req.GET.get('0firstFlightAirline', None)
    firstFlightArrivalAirport = req.GET.get('0firstFlightArrivalAirport', None)
    firstFlightArrivalDate = req.GET.get('0firstFlightArrivalDate', None)
    firstFlightArrivalDuration = req.GET.get('0firstFlightArrivalDuration', None)

    secondFlightDepartureAirport = req.GET.get('0secondFlightDepartureAirport', None)
    secondFlightDepartureDate = req.GET.get('0secondFlightDepartureDate', None)
    secondFlightAirlineLogo = req.GET.get('0secondFlightAirlineLogo', None)
    secondFlightAirline = req.GET.get('0secondFlightAirline', None)
    secondFlightArrivalAirport = req.GET.get('0secondFlightArrivalAirport', None)
    secondFlightArrivalDate = req.GET.get('0secondFlightArrivalDate', None)
    secondFlightArrivalDuration = req.GET.get('0secondFlightArrivalDuration', None)

    flight_total_duration = req.GET.get('flight_total_duration', None)
    flight_price = req.GET.get('flight_price', None)
    origin = req.GET.get('origin', None)
    short_Origin = req.GET.get('short_Origin', None)
    short_Destination = req.GET.get('short_Destination', None)
    long_Origin = req.GET.get('long_Origin', None)
    long_Destination = req.GET.get('long_Destination', None)
    destination = req.GET.get('destination', None)
    travellers = req.GET.get('travellers', None)
    # Extract flight variables from query parameters
    thirdFlightDepartureAirport = req.GET.get('1firstFlightDepartureAirport', None)
    thirdFlightDepartureDate = req.GET.get('1firstFlightDepartureDate', None)
    thirdFlightAirlineLogo = req.GET.get('1firstFlightAirlineLogo', None)
    thirdFlightAirline = req.GET.get('1firstFlightAirline', None)
    thirdFlightArrivalAirport = req.GET.get('1firstFlightArrivalAirport', None)
    thirdFlightArrivalDate = req.GET.get('1firstFlightArrivalDate', None)
    thirdFlightArrivalDuration = req.GET.get('1firstFlightArrivalDuration', None)

    fourthFlightDepartureAirport = req.GET.get('1secondFlightDepartureAirport', None)
    fourthFlightDepartureDate = req.GET.get('1secondFlightDepartureDate', None)
    fourthFlightAirlineLogo = req.GET.get('1secondFlightAirlineLogo', None)
    fourthFlightAirline = req.GET.get('1secondFlightAirline', None)
    fourthFlightArrivalAirport = req.GET.get('1secondFlightArrivalAirport', None)
    fourthFlightArrivalDate = req.GET.get('1secondFlightArrivalDate', None)
    fourthFlightArrivalDuration = req.GET.get('1secondFlightArrivalDuration', None)
    
    # Create a dictionary of flight details to pass to the template
    flight_data = {
        "firstFlightDepartureAirport": firstFlightDepartureAirport,
        "firstFlightDepartureDate": firstFlightDepartureDate,
        "firstFlightAirlineLogo": firstFlightAirlineLogo,
        "firstFlightAirline": firstFlightAirline,
        "firstFlightArrivalAirport": firstFlightArrivalAirport,
        "firstFlightArrivalDate": firstFlightArrivalDate,
        "firstFlightArrivalDuration": firstFlightArrivalDuration,
        "secondFlightDepartureAirport": secondFlightDepartureAirport,
        "secondFlightDepartureDate": secondFlightDepartureDate,
        "secondFlightAirlineLogo": secondFlightAirlineLogo,
        "secondFlightAirline": secondFlightAirline,
        "secondFlightArrivalAirport": secondFlightArrivalAirport,
        "secondFlightArrivalDate": secondFlightArrivalDate,
        "secondFlightArrivalDuration": secondFlightArrivalDuration,
        "thirdFlightDepartureAirport": thirdFlightDepartureAirport,
        "thirdFlightDepartureDate": thirdFlightDepartureDate,
        "thirdFlightAirlineLogo": thirdFlightAirlineLogo,
        "thirdFlightAirline": thirdFlightAirline,
        "thirdFlightArrivalAirport": thirdFlightArrivalAirport,
        "thirdFlightArrivalDate": thirdFlightArrivalDate,
        "thirdFlightArrivalDuration": thirdFlightArrivalDuration,
        "fourthFlightDepartureAirport": fourthFlightDepartureAirport,
        "fourthFlightDepartureDate": fourthFlightDepartureDate,
        "fourthFlightAirlineLogo": fourthFlightAirlineLogo,
        "fourthFlightAirline": fourthFlightAirline,
        "fourthFlightArrivalAirport": fourthFlightArrivalAirport,
        "fourthFlightArrivalDate": fourthFlightArrivalDate,
        "fourthFlightArrivalDuration": fourthFlightArrivalDuration,
        "flight_total_duration": flight_total_duration,
        "flight_price": flight_price,
        "origin": origin,
        "destination": destination,
        "short_Origin": short_Origin,
        "short_Destination": short_Destination,
        "long_Origin": long_Origin,
        "long_Destination": long_Destination,
        "travellers": travellers,
    }
    # Get the latest flight from the database
    user_id = req.user
    latest_flight = FlightTmp.objects.filter(user_id=user_id).latest('added')
    print("---------------------------------")
    print(latest_flight)

    return render(req, "flights-checkout-round.html", flight_data)

@csrf_exempt
def pre_Checkout(req):
    if req.method == "POST":
        flight_data = req.POST.get('flight', None)
        user_id = req.POST.get('user_id', None)      
        #save to database model FlightTmp
        print("passed")
        newflight = FlightTmp(flight_data=flight_data, user_id=user_id)
        newflight.save()
        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
