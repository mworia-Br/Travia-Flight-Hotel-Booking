from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib import messages

# Create your views here.

def faq(req):
    return render(req, 'faq.html')

def faq_hotel(req):
    return render(req, 'faq-hotel.html')

def about_us(req):
    return render(req, 'about-us.html')

def blog(req):
    return render(req, 'blog.html')

def promo(req):
    return render(req, 'promo.html')

def contact(req):
    return render(req, 'contact.html')

def guide(req):
    return render(req, 'guide.html')