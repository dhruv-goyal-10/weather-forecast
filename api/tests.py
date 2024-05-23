from django.test import TestCase
from django.test import TestCase
from .models import WeatherData
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from django.conf import settings


class WeatherDataTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("weather-data")

    def test_get_weather(self):
        response = self.client.get(
            self.url, {"lat": 33.441792, "lon": -94.037689, "detailing_type": "current"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_weather_data_model(self):
        weather_data = WeatherData.objects.create(
            lat=33.441792, lon=-94.037689, detailing_type="current", data={"temp": 20}
        )
        self.assertTrue(weather_data.is_recent())

    def test_weather_data_expiration(self):

        weather_data = WeatherData.objects.create(
            lat=33.441792,
            lon=-94.037689,
            detailing_type="current",
            data={"temp": 20},
        )
        minutes_to_subtract = int(settings.DATA_MAX_AGE_MINUTES) + 10
        weather_data._set_timestamp(
            timezone.now()
            - timezone.timedelta(minutes=minutes_to_subtract)
        )
        self.assertFalse(weather_data.is_recent())

    def test_invalid_lat_lon(self):
        response = self.client.get(
            self.url, {"lat": "invalid", "lon": "invalid", "detailing_type": "current"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid latitude or longitude values", response.data["error"])

        response = self.client.get(
            self.url, {"lat": 100, "lon": 200, "detailing_type": "current"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Latitude must be between -90 and 90", response.data["error"])

        response = self.client.get(
            self.url, {"lat": 45, "lon": 200, "detailing_type": "current"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Longitude must be between -180 and 180", response.data["error"])
        
    def test_invalid_detailing_type(self):
        response = self.client.get(
            self.url, {"lat": 33.441792, "lon": -94.037689, "detailing_type": "invalid"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid detailing type", response.data["error"])
