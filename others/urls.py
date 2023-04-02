from . import views
from django.urls import path, include

urlpatterns = [
    path('faqs/', views.faq, name="faq"),
    path('faq-hotels/', views.faq_hotel, name="faq_hotel"),
    path('blog/', views.blog, name="blog"),
    path('contact/', views.contact, name="contact"),
    path('guide/', views.guide, name="guide"),
    path('about-us/', views.about_us, name="about_us"),
    path('promo/', views.promo, name="promo"),
]