from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class CartItem(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=1000, primary_key=True)
    flight_data = models.JSONField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    made_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.username + self.id

class SearchedRoute(models.Model):
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    made_on = models.DateTimeField(auto_now_add=True)

admin.site.register(CartItem)
admin.site.register(SearchedRoute)