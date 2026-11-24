import requests
from django.shortcuts import render
from .forms import CityForm


def weather_home(request):
    weather_data = None
    error_message = None

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data["city"]
            api_url = f"https://api.example.com/weather?q={city}"
            try:
                response = requests.get(api_url, timeout=10)
                response.raise_for_status()
                weather_data = response.json()
            except Exception:
                weather_data = None
                error_message = "Could not fetch weather for that city. Please try again."
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