from django.db import models

class Restaurant(models.Model):
    restaurant_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    station = models.CharField(max_length=200, null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    #lunchprice = models.CharField(max_length=200)
    #dinnerprice = models.CharField(max_length=200)
    url = models.URLField()
    #created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.station})"
