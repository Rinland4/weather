from django.shortcuts import render
from .forms import CityForm
from urllib.request import urlopen
from urllib.parse import quote
import json


# Create your views here.
def weather_home(request):
    weather_data = None
    error_message = None

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data["city"]

            try:
                geocoding_url = (
                    "https://geocoding-api.open-meteo.com/v1/search"
                    f"?name={quote(city)}&count=1&language=en&format=json"
                )
                with urlopen(geocoding_url, timeout=10) as response:
                    location_data = json.loads(response.read().decode("utf-8"))

                locations = location_data.get("results", [])
                if not locations:
                    raise ValueError("City not found")

                location = locations[0]
                weather_url = (
                    "https://api.open-meteo.com/v1/forecast"
                    f"?latitude={location['latitude']}"
                    f"&longitude={location['longitude']}"
                    "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
                )
                with urlopen(weather_url, timeout=10) as response:
                    forecast_data = json.loads(response.read().decode("utf-8"))

                current = forecast_data["current"]
                weather_data = {
                    "city": location["name"],
                    "temperature": current["temperature_2m"],
                    "humidity": current["relative_humidity_2m"],
                    "wind": current["wind_speed_10m"],
                }
            except Exception:
                weather_data = None
                error_message = "Could not fetch weather for that city. Please try again later."
    else:
        form = CityForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
            "weather_data": weather_data,
            "error_message": error_message,
        },
    )
