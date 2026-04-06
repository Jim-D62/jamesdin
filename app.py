import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
if not API_KEY:
    import warnings
    warnings.warn(
        "OPENWEATHER_API_KEY environment variable is not set. "
        "Weather lookups will fail. Set it before starting the app.",
        RuntimeWarning,
        stacklevel=1,
    )
API_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city", "").strip()
    if not city:
        return render_template("index.html", error="Please enter a city name.")

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(API_URL, params=params, timeout=10)
    except requests.exceptions.RequestException:
        return render_template(
            "index.html", error="Network error. Please try again later."
        )

    if response.status_code == 404:
        return render_template(
            "index.html", error=f'City "{city}" not found. Please check the name and try again.'
        )
    if response.status_code != 200:
        return render_template(
            "index.html", error="Unable to fetch weather data. Please try again."
        )

    data = response.json()
    try:
        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"], 1),
            "icon": data["weather"][0]["icon"],
        }
    except (KeyError, IndexError, TypeError):
        return render_template(
            "index.html", error="Unexpected response from weather service. Please try again."
        )

    return render_template("index.html", weather=weather_data, searched_city=data["name"])


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
