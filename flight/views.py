from django.shortcuts import render
from amadeus import Client, ResponseError, Location
from django.http import JsonResponse
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