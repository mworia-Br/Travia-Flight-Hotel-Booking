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
                departureDate=departure_date, adults=1, oneWay=True)
            context = {
                "data": response.data
            }
            return JsonResponse(context)

        except ResponseError as error:
            print(error)
    else:
        return JsonResponse({"error": "Invalid request method"})

def search_offersRoundTrip(req):
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

@csrf_exempt
def flight_checkout(req):
    if req.method == "POST":
        try: 
            data = json.loads(req.body)
            flight = data.get('flight')
            render(req, 'flightcheckout.html', {'flight': flight})
        except ResponseError as error:
            print(error)
    else:
       return JsonResponse({"error": "Invalid request method"})

