from django.db import models

# Create your models here.
class FlightTmp(models.Model):
    user_id = models.CharField(max_length=100)
    flight_data = models.JSONField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user_id