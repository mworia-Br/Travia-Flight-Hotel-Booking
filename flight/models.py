from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class CartItem(models.Model):
    #owner=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    owner = models.CharField(max_length=100, null=True, blank=True)
    flight_data = models.JSONField(blank=True, null=True)
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
    stripe_payment_intent = models.CharField(max_length=200)
    updated_on = models.DateTimeField(blank=True, null=True)

    # This field can be changed as status
    has_paid = models.BooleanField(default=False, verbose_name='Payment Status')

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