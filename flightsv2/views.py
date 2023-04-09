import json
import io
import ast
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from .booking import Booking
from .models import FlightTmp
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from flight.models import CartItem, SearchedRoute
from django.shortcuts import redirect
from accounts.models import Traveller_Info
from payments.views import create_checkout_session
from django.urls import reverse

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
    if return_date:
        route = SearchedRoute.objects.create(
        origin=origin, 
        destination=destination, 
        departure_date=departure_date,
        return_date=return_date,
        adults_count=adults,
        children_count=children
        )
    else:
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
        "children": children
        #'currency': 'USD'
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
            if 'dictionaries' in search_flights.result:
                # Get the country code for the destination location
                country = search_flights.result['dictionaries'].get('locations').get(destination).get('countryCode', None)
                # Get the travel restrictions for the destination
                travel_restrictions = amadeus.duty_of_care.diseases.covid19_report.get(countryCode=country)
                if travel_restrictions.data['areaAccessRestriction']['declarationDocuments'] is not None:
                    documents = travel_restrictions.data['areaAccessRestriction']['declarationDocuments'].get('text', None)
                else:
                    documents = None
                try:
                    covid_tests = travel_restrictions.data['areaAccessRestriction']['travelTest']['travelTestConditionsAndRules'][0]['scenarios'][0]['condition']['textualScenario']
                except KeyError:
                    covid_tests = None
            else:
                # Handle the case where 'dictionaries' key is not present in search_flights.result
                country = None # or whatever value is appropriate for your use case
                # Get the travel restrictions for the destination
                travel_restrictions = None
                documents = None
                covid_tests = None
            
        except ResponseError as error:#handle the error here
            #messages.add_message(
            #    req, messages.ERROR, error.response.result["errors"][0]["detail"]
            #)
            return render(req, "flights-category-multi.html", {})
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
    return render(req, "flights-category-multi.html", {})


def book_flight(req, flight):
    # Create a fake traveler profile for booking
    traveller = Traveller_Info.objects.get(user=req.user).latest('id')
    traveler = traveller.traveler_list
    travelerfake = {
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
    flightDate = req.GET.get('flightDate', None)
    lastTicketingDate = req.GET.get('lastTicketingDate', None)
    bookableSeats = req.GET.get('bookableSeats', None)

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
        "flightDate": flightDate,
        "lastTicketingDate": lastTicketingDate,
        "bookableSeats": bookableSeats,
    }
    # Get the latest flight from the database
    user_id = req.user
    latest_flight = FlightTmp.objects.filter(user_id=user_id).latest('added')
    print("---------------------------------")
    flight_info = latest_flight.flight_data
    # save cart item with flight data
    new_item = CartItem.objects.create(owner=req.user, flight_data=flight_data, quantity=1)
    cleaned_flight1 = str(flight_info).replace("'", '"')
    cleaned_flight2 = str(cleaned_flight1).replace("False", 'false')
    cleaned_flight = str(cleaned_flight2).replace("True", 'true')
    print(cleaned_flight)
    buffer = io.StringIO()
    json.dump(cleaned_flight, buffer)
    print(type(buffer))
    buffer.seek(0)
    flight_info_json = json.load(buffer)
    # end of saving cart item && getting flight info
    print("---------------------------------")
    travelers = int(flight_data['travellers'])
    alltravelers = []
    for i in range(travelers):
        traveleritems = []
        # fill traveleritems = [] with a letters in the alphabet for each traveler
        traveleritems.append(chr(65 + i))
        alltravelers.append(traveleritems)

    print(alltravelers)

    context = {'flight_info_json': flight_info_json,
        'flight_data': flight_data,
        'traveleritems': alltravelers
    }
    return render(req, "flights-checkout-round.html", context)

@csrf_exempt
@login_required(login_url="/login")
def pre_Checkout(req):
    if req.method == "POST":
        flight_data = req.POST.get('flight', None)
        user_id = req.POST.get('user', None)
        if user_id is None:
            user_id = req.user      
        # save to database model FlightTmp
        print("passed")
        newflight = FlightTmp(flight_data=flight_data, user_id=user_id)
        newflight.save()
        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})

@login_required(login_url="/login")
def checkout_step2(req):
    flight = CartItem.objects.filter(owner=req.user).latest('made_on')
    flight_data = flight.flight_data
    travelers = int(flight.flight_data['travellers'])
    print(flight.flight_data['travellers'])
    alltravelers = []
    for i in range(travelers):
        traveleritems = []
        # fill traveleritems = [] with a letters in the alphabet for each traveler
        traveleritems.append(chr(65 + i))
        alltravelers.append(traveleritems)

    print(alltravelers)
    context = {'flight_data': flight_data, 'traveleritems': alltravelers}
    return render(req, 'flights-checkout-step2.html', context)

@login_required(login_url="/login")
def checkout_traveler(req):
    if req.method == 'POST':
        cartitem = CartItem.objects.filter(owner=req.user).latest('made_on')
        get_id = cartitem.id
        num_travelers = int(cartitem.flight_data['travellers'])
         # Extract message for the host
        traveler_message = req.POST.get('message')
        # Initialize an empty list to hold all the traveler dictionaries
        traveler_list = []
        # Loop over the range of the number of travelers to extract data for each one
        for i in range(num_travelers):
            # Initialize an empty dictionary for each traveler
            traveler = {}
            # Extract the data from the form for this traveler and populate the dictionary
            traveler['id'] = req.POST.get('id')
            traveler['name'] = {
                'firstName': req.POST.get('fname{}'.format(i)),
                'lastName': req.POST.get('lname{}'.format(i))
            }
            traveler['dateOfBirth'] = req.POST.get('dob{}'.format(i))
            traveler['gender'] = req.POST.get('gender{}'.format(i))
            traveler['contact'] = {
                'emailAddress': req.POST.get('email{}'.format(i)),
                'phones': [
                    {
                        'deviceType': 'MOBILE',
                        'countryCallingCode': req.POST.get('phone_country{}'.format(i)),
                        'number': req.POST.get('phone{}'.format(i))
                    }
                ]
            }
            traveler['documents'] = [
                {
                    'documentType': req.POST.get('document_type{}'.format(i)),
                    'birthPlace': '',
                    'issuanceLocation': '',
                    'issuanceDate': '',
                    'number': req.POST.get('document_number{}'.format(i)),
                    'expiryDate': '',
                    'issuanceCountry': '',
                    'validityCountry': '',
                    'nationality': '',
                    'holder': True,
                }
            ]
            # Add this traveler's dictionary to the list
            traveler_list.append(traveler)
        # Return the traveler list as a response
        print("handling")
        new_travellerinfo = Traveller_Info.objects.create(owner=req.user, flight_id=get_id, traveler_message=traveler_message, traveler_list=traveler_list)
        print('traveler_list processed')
        
        #data to be sent to the payment_view
        customer_email = req.user.email
        payment_method_types=['card']
        product_name = cartitem.flight_data['short_Origin'] + " - " + cartitem.flight_data['short_Destination']
        unit_amount_f = float(cartitem.flight_data['flight_price']) * 100
        unit_amount = int(unit_amount_f)
        # pass data to payment_view
        get_id = get_id
        # Save the data in the session
        req.session['get_id'] = get_id
        req.session['customer_email'] = customer_email
        req.session['payment_method_types'] = payment_method_types
        req.session['product_name'] = product_name
        req.session['unit_amount'] = unit_amount

        # Redirect to the other view
        url = reverse('start_payment')
        return redirect(url)
