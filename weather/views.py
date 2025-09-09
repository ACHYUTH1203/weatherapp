from django.shortcuts import render
import requests

def index(request):
    weather_data = None
    error = None

    if request.method == "POST":
        city = (request.POST.get("city") or "").strip()

        if city:
            api_key = "e4451dcdfc7707a714b8746ca5eaa652"  #"PROVIDE API KEY"
            try:
                r = requests.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params={"q": city, "appid": api_key, "units": "metric"},
                    timeout=10,
                )
                r.raise_for_status()
                data = r.json()

              
                if str(data.get("cod")) == "200":
                    weather_data = {
                        "city": data.get("name", city).title(),
                        "temp": float(data["main"]["temp"]),
                        "description": data["weather"][0]["description"].title(),
                        "country": data["sys"]["country"],
                        "humidity": int(data["main"]["humidity"]),
                     
                        "wind_speed": round(float(data["wind"]["speed"]) * 3.6, 1),
                    }
                else:
                    error = data.get("message", "City not found.")
            except requests.exceptions.RequestException:
                error = "Unable to fetch weather right now. Please try again."
        else:
            error = "Please enter a city."

    return render(request, "weather/index.html", {"weather": weather_data, "error": error})
