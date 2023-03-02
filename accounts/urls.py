from . import views
from django.urls import path
urlpatterns = [
    path('', views.Index, name="index"),
    path('login/', views.Login, name="login"),
]