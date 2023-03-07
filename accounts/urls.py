from . import views
from django.urls import path
urlpatterns = [
    path('', views.Index, name="index"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('oneway_flight_search/', views.oneway_view, name='oneway_flight'),
    path('roundtrip_flight_search/', views.roundtrip_view, name='roundtrip_flight'),
    path('hotels/', views.hotels_view, name='hotels'),
    path('profile/', views.profile_view, name='profile'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('forgot_password/',views.forgot_password_view, name='forgot_password'),
    path('set-password/<str:token>/', views.set_password, name='set_password'),
]