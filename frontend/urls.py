from . import views
from django.urls import path
urlpatterns = [
    path('', views.Indexfr, name="testhome"),
    path('frontend/', views.Frontend, name='hometest'),
    path('origin_airport_search/', views.origin_airport_search, name='origin_airport_search'),
    path('destination_airport_search/', views.destination_airport_search, name='destination_airport_search'),
    #path('book_flight/<str:flight>/', views.book_flight, name='book_flight'),
]