from django.urls import path
from . import views

urlpatterns = [
    path('select_destination/<str:param>',
         views.select_destination, name="select_destination"),
    path('search_offers/', views.search_offers, name="search_offers"),
    path('search_roundtrip/', views.search_roundtrip, name="search_roundtrip"),
    path('price_offers', views.price_offer, name="price_offer"),
    path('book_flight/', views.book_flight, name="book_flight"),
    path('flight_checkout/', views.flight_checkout, name="flight_checkout"),
]