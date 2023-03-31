from django.urls import path

from . import views

urlpatterns = [
    path('start_payment/', views.create_checkout_session, name='start_payment'),
]