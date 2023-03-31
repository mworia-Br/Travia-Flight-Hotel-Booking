from django.urls import path

from . import views
from .views import PaymentSuccessView, PaymentFailedView

urlpatterns = [
    #path('start_payment/<int:get_id>/<str:customer_email>/<str:payment_method_types>/<str:product_name>/<int:unit_amount>/', views.create_checkout_session, name='start_payment'),
    path('start_payment/', views.create_checkout_session, name='start_payment'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
]