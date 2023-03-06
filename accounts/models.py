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

class Traveler(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    birth_date = models.DateField()
    city = models.CharField(max_length=50)
    passport_holder = models.BooleanField(default=False)
    passport_number = models.CharField(max_length=20)
    passport_issue_date = models.DateField()
    passport_expiry = models.DateField()
    passport_country = models.CharField(max_length=50)
    passport_validitycountry = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + self.last_name + self.nationality

admin.site.register(OneWayFlightSearch)
admin.site.register(TwoWayFlightSearch)
admin.site.register(HotelSearch)
admin.site.register(Traveler)