from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_weather_data


class WeatherDataAPIView(APIView):

    def get(self, request):

        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        detailing_type = request.query_params.get("detailing_type")

        if not all([lat, lon, detailing_type]):
            return Response(
                {"success": False, "error": "Missing parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response(
                {"success": False, "error": "Invalid latitude or longitude values"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not (-90 <= lat <= 90):
            return Response(
                {"success": False, "error": "Latitude must be between -90 and 90"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not (-180 <= lon <= 180):
            return Response(
                {"success": False, "error": "Longitude must be between -180 and 180"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        possible_detailing_types = ["current", "minutely", "hourly", "daily"]
        if detailing_type not in possible_detailing_types:
            return Response(
                {"success": False, "error": "Invalid detailing type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = get_weather_data(lat, lon, detailing_type)
        if data:
            return Response({"success": True, "data": data})

        return Response(
            {"success": False, "error": "An unexpected error occured."}, status=400
        )
