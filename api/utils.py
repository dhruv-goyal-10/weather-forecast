import requests
from django.conf import settings
from .models import WeatherData

OPENWEATHERMAP_API_KEY = settings.OPENWEATHERMAP_API_KEY


def get_weather_data(lat, lon, detailing_type):
    """
    Returns the weather data for the given latitude, longitude, and detailing type.
    If the data is not recent, it fetches the data from the OpenWeatherMap API.
    """
    
    weather_data = (
        WeatherData.objects.filter(lat=lat, lon=lon, detailing_type=detailing_type)
        .order_by("-timestamp")
        .first()
    )

    if weather_data and weather_data.is_recent():
        return weather_data.data

    success, api_data = fetch_data(lat, lon)
    
    if not success:
        return None

    weather_data_to_save = list()

    possible_detailing_types = ["current", "minutely", "hourly", "daily"]
    
    # Fetching all the data from the API and saving it to the database, 
    # regardless of the detailing type demanded by the user.
    
    for detailing_type in possible_detailing_types:
        data = api_data[detailing_type]
        weather_data = WeatherData(
            lat=lat, lon=lon, detailing_type=detailing_type, data=data
        )
        weather_data_to_save.append(weather_data)

    WeatherData.objects.bulk_create(weather_data_to_save)

    
    # For some places the API does not return all the detailing types.
    if detailing_type in api_data:
        return api_data[detailing_type]
    return None

def fetch_data(lat, lon) -> tuple[int, dict]:
    """
    Fetches the weather data from the OpenWeatherMap API.
    Returns a tuple of success status and the data.
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    data = response.json()
    return status_code, data
