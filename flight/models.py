from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class CartItem(models.Model):
    #owner=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.CharField(max_length=100, null=True, blank=True)
    flight_data = models.JSONField()
    quantity = models.PositiveIntegerField(default=1)
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="Waiting")
    created_at = models.DateTimeField(auto_now_add=True)
    made_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner + self.status

class SearchedRoute(models.Model):
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    adults_count = models.PositiveIntegerField(default=1)
    children_count = models.PositiveIntegerField(default=0)
    infants_count = models.PositiveIntegerField(default=0)
    made_on = models.DateTimeField(auto_now_add=True)

admin.site.register(CartItem)
admin.site.register(SearchedRoute)