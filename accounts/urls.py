from . import views
from django.urls import path
urlpatterns = [
    path('', views.Index, name="index"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_view, name='logout'),
]