import json
import ast
import stripe
import time
from requests.exceptions import ConnectionError
from django.conf import settings
from amadeus import Client, ResponseError, Location
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone
from flightsv2.flight import Flight
from flightsv2.booking import Booking
from flightsv2.models import FlightTmp
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from flight.models import CartItem, SearchedRoute
from django.views.generic import ListView, CreateView, DetailView, TemplateView

# Create your views here.
def detailView(req):
    pass

@csrf_exempt
def create_checkout_session(req):
    # Get the data from the session
    get_id = req.session.get('get_id')
    customer_email = req.session.get('customer_email')
    payment_method_types = req.session.get('payment_method_types')
    product_name = req.session.get('product_name')
    unit_amount = req.session.get('unit_amount')
    
    # Clear the session data
    del req.session['get_id']
    del req.session['customer_email']
    del req.session['payment_method_types']
    del req.session['product_name']
    del req.session['unit_amount']

    cartitem = CartItem.objects.get(id=get_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    # Set the maximum number of retries and the delay between each retry attempt
    max_retries = 3
    retry_delay = 1  # seconds
    
    for retry_count in range(max_retries):
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email = customer_email,
                payment_method_types=payment_method_types,
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                            'name': product_name,
                            'description': 'Flight Booking Payment for ' + product_name + 'flight',
                            'images': ['https://www.airtravia.co.ke/static/img/logo-light.svg'],
                            },
                            'unit_amount': unit_amount,
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=req.build_absolute_uri(
                    reverse('success')
                ) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=req.build_absolute_uri(reverse('failed')),
            )
            break  # Exit the loop if the req is successful
        except ConnectionError:
            if retry_count == max_retries - 1:
                raise  # Raise an exception if all retries have failed
            else:
                time.sleep(retry_delay)
                continue  # Retry the req after a short delay
    
    
    flight_data = cartitem.flight_data
    cartitem.stripe_payment_intent = checkout_session['payment_intent']
    cartitem.updated_on = timezone.now()
    cartitem.save()
    print("working")
    return render(req, 'flights-checkout-pay.html', {
        'flight_data': flight_data,
        'session_id': checkout_session.id,
        })

class PaymentSuccessView(TemplateView):
    template_name = "payment_success.html"

    def get(self, req, *args, **kwargs):
        session_id = req.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        #order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order = CartItem.objects.get(stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(req, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "payment_failed.html"