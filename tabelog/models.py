from django.db import models

class Restaurant(models.Model):
    restaurant_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    station = models.CharField(max_length=200, null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=500)

    
    def __str__(self):
        return f"{self.name} ({self.station})"
