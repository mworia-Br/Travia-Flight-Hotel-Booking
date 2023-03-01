from django.urls import path
from . import views
urlpatterns = [
    path('select_destination/<str:param>', views.select_destination,
            name="select_destination"),
]