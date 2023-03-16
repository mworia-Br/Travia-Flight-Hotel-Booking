from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index, name="index"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('oneway-flight/', views.oneway_view, name='oneway_flight'),
    path('roundtrip-flight/', views.roundtrip_view, name='roundtrip_flight'),
    path('hotels/', views.hotels_view, name='hotels'),
    path('profile/', views.profile, name='profile'),
    path('forgot-password/',views.forgot_password_view, name='forgot_password'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('set-password/<str:uidb64>/<str:token>/', views.set_password, name='set_password'),
    path('orders/', views.profile_orders, name='orders'),
    path('travelers/', views.profile_travelers, name='travelers'),
    path('add-traveler/', views.profile_traveleradd, name='add_traveler'),
]