from django.contrib import admin
from .models import WeatherPattern
# Register your models here.

# class PestPredictionAdmin(admin, ModelAdmin):
#     list_display = ('id','name')
# admin.site.register(WeatherPattern,PestPredictionAdmin)

admin.site.register(WeatherPattern)