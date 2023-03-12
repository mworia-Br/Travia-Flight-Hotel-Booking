from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
            print(origin_code, destination_code, departure_date)
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_code, destinationLocationCode=destination_code, 
                departureDate=departure_date, adults=1)
            context = {
                "data": response.data
            }
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
            flight = data.get("dataflight")
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

def flight_checkout(req):
    if req.method == "POST":
        try: 
            data = json.loads(req.dataflight)
            flight = data.get('dataflight')
            render(req, 'flightcheckout.html', {'flight': flight})
        except ResponseError as error:
            print(error)
    else:
       return JsonResponse({"error": "Invalid request method"})

# Hotel views.py

# Define a function to search for hotels
def search_hotels(req):
    if req.method == "GET":
        try:
            checkin = req.GET["checkInDate"]
            checkout = req.GET["checkout"]
            cityCode = req.GET["locationCode"]
            adults = req.GET["adultsPerRoom"]
            children = req.GET["childrenPerRoom"]
            rooms = req.GET["rooms"]
            
            # Define API endpoint and parameters
            #url = 'https://api.sandbox.amadeus.com/v1.2/hotels/search-circle'
            
            # Send GET request to API
            response = amadeus.shopping.hotel_offers_search.get(cityCode=cityCode, checkInDate=checkin, checkOutDate=checkout, adults=adults, radius=5, radiusUnit='KM', currency='USD')
            
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
