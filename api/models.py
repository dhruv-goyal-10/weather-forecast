from django.db import models
from django.utils import timezone
from django.conf import settings

class WeatherData(models.Model):

    DETAILING_CHOICES = [
        ("current", "current"),
        ("minutely", "minutely"),
        ("hourly", "hourly"),
        ("daily", "daily"),
    ]
    
    lat = models.FloatField()
    lon = models.FloatField()
    detailing_type = models.CharField(max_length=20, choices=DETAILING_CHOICES)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_recent(self, max_age_minutes=settings.DATA_MAX_AGE_MINUTES):
        return timezone.now() - self.timestamp < timezone.timedelta(
            minutes=max_age_minutes
        )
        
    def _set_timestamp(self, new_timestamp):
        """Set the timestamp to a custom value (for testing purposes)."""
        self.timestamp = new_timestamp
        self.save()
