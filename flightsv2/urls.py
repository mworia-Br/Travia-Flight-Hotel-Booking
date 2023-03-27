from django.urls import path

from . import views

urlpatterns = [
    path('search_flights/', views.search_flights, name='search_flights'),
    path('book_flight/<str:flight>/', views.book_flight, name='book_flight'),
    path('checkoutHandle/', views.checkoutHandle, name='checkoutHandle'),
    path('pre_checkout/', views.pre_Checkout, name='pre_checkout'),
    path('checkout_step2/', views.checkout_step2, name='checkout_step2'),
    path('checkout_step3/', views.checkout_step3, name='checkout_step3'),
]
