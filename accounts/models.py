from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Personal_Info(models.Model):
    user= models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=True)
    surname = models.CharField(max_length=50, blank=False, null=True)
    phone = models.CharField(max_length=20, blank=False, null=True)
    email = models.EmailField(max_length=254, blank=False, null=True)
    city = models.CharField(max_length=50, blank=False, null=True)
    natianality = models.CharField(max_length=50, blank=False, null=True)
    bio = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + self.surname + self.natianality

class Traveler(models.Model):
    user=models.CharField(max_length=100, null=True, blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=False, null=True)
    name = models.CharField(max_length=50, blank=False, null=True)
    surname = models.CharField(max_length=50, blank=False, null=True)
    date_of_birth = models.DateField(blank=False, null=True)
    document_type = models.CharField(max_length=50, null=True)
    nationality = models.CharField(max_length=50, blank=False, null=True)
    email = models.EmailField(max_length=254, blank=False, null=True)
    phone = models.CharField(max_length=20, blank=False, null=True)
    id_card_number = models.CharField(max_length=20, blank=False, null=True)
    id_card_expiry = models.DateField(blank=True, null=True)
    id_card_country = models.CharField(max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    passport_issuanceDATE = models.DateField(max_length=20, blank=True, null=True)
    passport_expiry = models.DateField(max_length=20, blank=True, null=True)
    passport_country = models.CharField(max_length=50, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name + self.surname + self.nationality

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

class Payment(models.Model):
    user=models.CharField(max_length=100, null=True, blank=True)
    method = models.CharField(max_length=50, blank=False, null=True)
    vendorCode = models.CharField(max_length=50, blank=False, null=True)
    cardNumber = models.CharField(max_length=50, blank=False, null=True)
    cardHolderName = models.CharField(max_length=50, blank=False, null=True)
    expiryMonth = models.CharField(max_length=50, blank=False, null=True)

    def __str__(self):
        return self.user + self.method + self.vendorCode

class Traveller_Info(models.Model):
    owner=models.CharField(max_length=100, null=True, blank=True)
    flight_id = models.CharField(max_length=50, blank=False, null=True)
    traveler_message = models.CharField(max_length=50, blank=False, null=True)
    traveler_list = models.CharField(max_length=5000, blank=False, null=True)

admin.site.register(HotelSearch)
admin.site.register(Traveler)
admin.site.register(Personal_Info)
admin.site.register(Payment)
admin.site.register(Traveller_Info)