from django.shortcuts import render
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CartItem, SearchedRoute
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .hotel import Hotel
from .room import Room

from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='zUlxNy4Kc6l5oSALcurajPCAUaYpDq1s',
    client_secret='K95GQ2APHlRQ0R1l'
)

def select_destination(req, param):
    if req.method == "GET":
        try:
           
            response = amadeus.reference_data.locations.get(
                keyword=param, subType=Location.ANY)
            context = {
                "data": response.data
            }
            return JsonResponse(context)

        except ResponseError as error:
            print(error)
    return JsonResponse({"error": "Invalid request method"})


def search_offers(req):
    if req.method == "GET":
        try:
            origin_code = req.GET["originCode"]
            destination_code = req.GET["destinationCode"]
            departure_date = req.GET["departureDate"]
            adults = req.GET["adults"]
            children = req.GET["children"]
            infants = req.GET["infants"]
            #currencyCode = USD
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_code, destinationLocationCode=destination_code, 
                departureDate=departure_date, adults=adults, children=children, infants=infants)
            context = {
                "data": response.data
            }
            # Create a new SearchedRoute object and save it to the database
            route = SearchedRoute.objects.create(
                origin=origin_code, 
                destination=destination_code, 
                departure_date=departure_date,
                adults_count=adults,
                children_count=children,
                infants_count=infants
            )
            return JsonResponse(context)

        except ResponseError as error:
            print(error)
    else:
        return JsonResponse({"error": "Invalid request method"})

def search_roundtrip(req):
    if req.method == "GET":
        try:
            origin_code = req.GET["originCode"]
            destination_code = req.GET["destinationCode"]
            departure_date = req.GET["departureDate"]
            return_date = req.GET["returnDate"]

            print(origin_code, destination_code, departure_date)
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_code, destinationLocationCode=destination_code, departureDate=departure_date, returnDate=return_date, adults=1)
            context = {
                "data": response.data
            }
            return JsonResponse(context)

        except ResponseError as error:
            print(error)
    else:
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def price_offer(req):
    if req.method == "POST":
        try:
            data = json.loads(req.body)
            flight = data.get("flight")
            response = amadeus.shopping.flight_offers.pricing.post(flight)
 
            return JsonResponse(response.data)

        except ResponseError as error:
            print(error)
    else:
       return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def book_flight(req):
    if req.method == "POST":
        try: 
            data = json.loads(req.body)
            flight = data.get('flight')
            traveler = data.get('traveler')
            booking = amadeus.booking.flight_orders.post(flight, traveler)
            return JsonResponse(booking)
        except ResponseError as error:
            print(error)
    else:
       return JsonResponse({"error": "Invalid request method"})

def addCartItem(request, flight_data):
    try:
        cart_item = CartItem.objects.create(owner=request.user, flight_data=flight_data, quantity=1)
        print("run")
        return JsonResponse({"success": "Item added to cart"})
    except:
        return JsonResponse({"error": "Item not added to cart"})


@login_required
def flight_checkout(req):
    if req.method == "GET":
        try:
            origin_code = req.GET["originCode"]
            destination_code = req.GET["destinationCode"] 
            short_Origin = req.GET["shortOrigin"]
            short_Destination = req.GET["shortDestination"]
            long_Origin = req.GET["longOrigin"]
            long_Destination = req.GET["longDestination"]
            departure_date = req.GET["departureDate"]
            arrival_date = req.GET["arrivalDate"]
            departure_Time = req.GET["departureTime"]
            arrival_Time = req.GET["arrivalTime"]
            flight_Duration = req.GET["flightDuration"]
            air_lineCode = req.GET["airlineCode"]
            logo_Url = req.GET["logoUrl"]
            bookable_Seats = req.GET["bookableSeats"]
            last_Ticketing = req.GET["lastTicketing"]
            adults_count = req.GET["adults"]
            children_count = req.GET["children"]
            infants_count = req.GET["infants"]
            flight_Total = req.GET["flightTotal"]
            traveler_s = adults_count + children_count + infants_count

            # Create a dictionary of flight details to pass to the template
            flight_data = {
                'origin_code': origin_code,
                'destination_code': destination_code,
                'short_origin': short_Origin,
                'short_destination': short_Destination,
                'long_origin': long_Origin,
                'long_destination': long_Destination,
                'departure_date': departure_date,
                'arrival_date': arrival_date,
                'departure_time': departure_Time,
                'arrival_time': arrival_Time,
                'flight_duration': flight_Duration,
                'airline_code': air_lineCode,
                'logo_url': logo_Url,
                'bookable_seats': bookable_Seats,
                'last_ticketing': last_Ticketing,
                'travelers': traveler_s,
                'adults_count': adults_count,
                'children_count': children_count,
                'infants_count': infants_count,
                'flight_total': flight_Total
            }
            # Add the flight to the cart
            new_item = CartItem.objects.create(owner=req.user, flight_data=flight_data, quantity=1)
            owner=req.user
            print(owner)
            #addCartItem(flight_data)
            return render(req, 'flights-checkout.html', flight_data)
        
        except:
            # Handle the exception appropriately
            print("errorincheckout")
    else:
        return render(req, 'flights-checkout.html')


# Hotel views.py

# Define a function to search for hotels
def search_hotels1(req):
    if req.method == "GET":
        try:
            checkin = req.GET["checkInDate"]
            checkout = req.GET["checkout"]
            cityCode = req.GET["locationCode"]
            adults = req.GET["adultsPerRoom"]
            children = req.GET["childrenPerRoom"]
            
            # Define API endpoint and parameters
            #url = 'https://api.sandbox.amadeus.com/v1.2/hotels/search-circle'
            
            # Send GET request to API
            response = amadeus.shopping.hotel_offers_search.get(cityCode=cityCode, checkInDate=checkin, checkOutDate=checkout, adults=adults, children=children, radius=30, radiusUnit='KM', currency='USD')
            
            # Check if request was successful
            if response.status_code == 200:
                context = {
                    "data": response.data
                }
                return JsonResponse(context)  
            else:
                # Request was not successful, return None
                return None

        except ResponseError as error:
            print(error)

def search_hotels(req):
    if req.method == "GET":
        checkin = req.GET["checkInDate"]
        checkout = req.GET["checkout"]
        cityCode = req.GET["locationCode"]
        adults = req.GET["adultsPerRoom"]
        children = req.GET["childrenPerRoom"]
        rooms = req.GET["rooms"]

        if cityCode and checkin and checkout:
            try:
                # Hotel List
                hotel_list = amadeus.reference_data.locations.hotels.by_city.get(cityCode=cityCode)
            except ResponseError as error:
                messages.add_message(req, messages.ERROR, error.response.body)
                return render(req, 'hotels', {})
            hotel_offers = []
            hotel_ids = []
            for i in hotel_list.data:
                hotel_ids.append(i['hotelId'])
            num_hotels = 40
            kwargs = {'hotelIds': hotel_ids[0:num_hotels],
                'checkInDate': req.POST.get('checkInDate'),
                'checkOutDate': req.POST.get('checkout')}
            try:
                # Hotel Search
                search_hotels = amadeus.shopping.hotel_offers_search.get(**kwargs)
            except ResponseError as error:
                messages.add_message(req, messages.ERROR, error.response.body)
                return render(req, 'hotels', {})
            try:
                for hotel in search_hotels.data:
                    offer = Hotel(hotel).construct_hotel()
                    hotel_offers.append(offer)
                    response = zip(hotel_offers, search_hotels.data)
                    context = {
                        "data": response.data
                    }
                return JsonResponse(context)

            except UnboundLocalError:
                messages.add_message(req, messages.ERROR, 'No hotels found.')
                return render(req, 'hotels', {})
        return render(req, 'hotels', {})


def rooms_per_hotel(request, hotel, departureDate, returnDate):
    try:
        # Search for rooms in a given hotel
        rooms = amadeus.shopping.hotel_offers_search.get(hotelIds=hotel,
                                                           checkInDate=departureDate,
                                                           checkOutDate=returnDate).data
        hotel_rooms = Room(rooms).construct_room()
        return render(request, 'demo/rooms_per_hotel.html', {'response': hotel_rooms,
                                                             'name': rooms[0]['hotel']['name'],
                                                             })
    except (TypeError, AttributeError, ResponseError, KeyError) as error:
        messages.add_message(request, messages.ERROR, error)
        return render(request, 'demo/rooms_per_hotel.html', {})


def book_hotel(request, offer_id):
    try:
        # Confirm availability of a given offer
        offer_availability = amadeus.shopping.hotel_offer_search(offer_id).get()
        if offer_availability.status_code == 200:
            guests = [{'id': 1, 'name': {'title': 'MR', 'firstName': 'BOB', 'lastName': 'SMITH'},
                       'contact': {'phone': '+33679278416', 'email': 'bob.smith@email.com'}}]

            payments = {'id': 1, 'method': 'creditCard',
                        'card': {'vendorCode': 'VI', 'cardNumber': '4151289722471370', 'expiryDate': '2023-08'}}
            booking = amadeus.booking.hotel_bookings.post(offer_id, guests, payments).data
        else:
            return render(request, 'demo/booking.html', {'response': 'The room is not available'})
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, 'demo/booking.html', {})
    return render(request, 'demo/booking.html', {'id': booking[0]['id'],
                                                 'providerConfirmationId': booking[0]['providerConfirmationId']
                                                 })