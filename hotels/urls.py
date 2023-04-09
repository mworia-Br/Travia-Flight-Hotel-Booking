from django.urls import path
from . import views

urlpatterns = [
    path('search_hotels/', views.search_hotels, name='search_hotels'),
    path('book_hotel/<str:offer_id>', views.book_hotel, name='book_hotel'),
    path('rooms_per_hotel/<str:hotel>/<str:departureDate>/<str:returnDate>/<int:adults>/<int:children>/<int:roomsqty>/', views.rooms_per_hotel, name='rooms_per_hotel')
]