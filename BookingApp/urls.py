"""BookingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

admin.site.site_header  =  "Airtravia admin"  
admin.site.site_title  =  "Airtravia admin site"
admin.site.index_title  =  "Airtravia Admin"

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('api/v1/flight/', include('flight.urls')),
    path('api/v2/flight/', include('flightsv2.urls')),
    path('api/v1/hotel/', include('hotels.urls')),
    path('booking/', include('frontend.urls')),
    path('', include('accounts.urls')),
    path('singleauth/', include('allauth.urls')),
    path('payment/', include('payments.urls')),
    path('logout', LogoutView.as_view()),
]
