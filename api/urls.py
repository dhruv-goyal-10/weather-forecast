from django.contrib import admin
from django.urls import path, include
from .views import WeatherDataAPIView

urlpatterns = [
    path("weather-data/", WeatherDataAPIView.as_view(), name="weather-data"),
]
