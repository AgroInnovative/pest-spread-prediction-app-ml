from django.db import models

# Create your models here.
class WeatherPattern(models.Model):
     name=models.CharField(max_length=250)
     temperature=models.FloatField()
     windSpeed=models.FloatField()
     humidity=models.FloatField()
     windBarrier=models.FloatField()
     visibility=models.FloatField()
     preassure = models.FloatField()
     
    #   