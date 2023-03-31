import json
import ast
import stripe
from django.conf import settings
from amadeus import Client, ResponseError, Location
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone
from flightsv2.flight import Flight
from flightsv2.booking import Booking
from flightsv2.models import FlightTmp
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from flight.models import CartItem, SearchedRoute

# Create your views here.
def detailView(req):
    pass

@csrf_exempt
def create_checkout_session(req, customer_email, payment_method_types, product_name, unit_amount, get_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = customer_email,
        payment_method_types=payment_method_types,
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': product_name,
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )
    cartitem = CartItem.objects.get(id=get_id)
    flight_data = cartitem.flight_data
    cartitem.stripe_payment_intent = checkout_session['payment_intent']
    cartitem.updated_on = timezone.now()
    cartitem.save()
    return render(request, 'flights-checkout-pay.html', {
        'flight_data': flight_data,
        'session_id': session.id,
    })

def success(req):
    return render(req, 'index.html')

def failed(req):
    return render(req, 'hotels.html')