from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class OneWayFlightSearch(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    departure_date = models.DateField()
    travel_class = models.CharField(max_length=10, default='all')
    non_stop = models.BooleanField(default=False)
    adults = models.IntegerField()
    children = models.IntegerField()
    infants = models.IntegerField()
    currency = models.CharField(max_length=3)
    max_price = models.IntegerField()
    made_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.origin + self.destination

class TwoWayFlightSearch(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    departure_date = models.DateField()
    travel_class = models.CharField(max_length=10, default='all')
    non_stop = models.BooleanField(default=False)
    return_date = models.DateField()
    adults = models.IntegerField()
    children = models.IntegerField()
    infants = models.IntegerField()
    currency = models.CharField(max_length=3)
    max_price = models.IntegerField()
    made_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.origin + self.destination

class HotelSearch(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=3)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField()
    children = models.IntegerField()
    currency = models.CharField(max_length=3)
    max_price = models.IntegerField()
    made_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination

admin.site.register(OneWayFlightSearch)
admin.site.register(TwoWayFlightSearch)