from django.urls import path

from . import views
from .views import PaymentSuccessView, PaymentFailedView

urlpatterns = [
    path('start_payment/', views.create_checkout_session, name='start_payment'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
]