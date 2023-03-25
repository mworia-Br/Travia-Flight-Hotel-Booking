from django.db import models

# Create your models here.
class FlightTmp(models.Model):
    user_id = models.CharField(max_length=100)
    flight_data = models.TextField(max_length=6000)
    added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user_id