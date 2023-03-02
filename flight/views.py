from django.shortcuts import render
from amadeus import Client, ResponseError, Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

amadeus = Client(
    client_id='Web App API Key',
    client_secret='Web App API Secret'
)

def select_destination(req, param):
    if req.method == "GET":
        try:
            print(param)
            response = amadeus.reference_data.locations.get(
                keyword=param, subType=Location.ANY)
            context = {
                "data": response.data
            }
            return JsonResponse(context)
        except ResponseError as error:
            print(error)
    else:
        return JsonResponse({"error": "Invalid request method"})

def search_offers(req):
    if req.method == "GET":
        try:
            response = amadeus.shopping.flight_offers.get(
                originLocationCode=req.GET.get("origin"),
                destinationLocationCode=req.GET.get("destination"),
                departureDate=req.GET.get("departureDate"),
                adults=req.GET.get("adults"),
                nonStop=req.GET.get("nonStop"),
                max=req.GET.get("max")
            )
            context = {
                "data": response.data
            }
            return JsonResponse(context)
        except ResponseError as error:
            print(error)

@csrf_exempt
def price_offer(req):
    if req.method == "POST":
        try:
            #flight = req.POST["flight"]
            data = json.loads(req.body)
            flight = data.get("flight")
            response = amadeus.shopping.flight_offers.pricing.post(
                flight)
            print(response.data)
            return JsonResponse(response.data)
        except ResponseError as error:
            print(error)
    else:
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def book_flight(req):
    if req.method == "POST":
        try:
            #flight = req.POST["flight"]
            data = json.loads(req.body)
            flight = data.get("flight")
            traveler = req.POST["traveler"]
            booking = amadeus.booking.flight_orders.post(
                flight, traveler)
            return JsonResponse(booking)
        except ResponseError as error:
            print(error)
    else:
        return JsonResponse({"error": "Invalid request method"})