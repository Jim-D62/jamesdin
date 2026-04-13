import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str) -> dict:
    """Fetch weather data for the given city from OpenWeatherMap."""
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }
    response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"], 1),
            "icon": data["weather"][0]["icon"],
            "error": None,
        }
    elif response.status_code == 404:
        return {"error": f"City '{city}' not found. Please check the spelling and try again."}
    elif response.status_code == 401:
        return {"error": "Invalid API key. Please set the OPENWEATHER_API_KEY environment variable."}
    else:
        return {"error": f"Unable to fetch weather data (status {response.status_code}). Please try again later."}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", weather=None, query="")


@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city", "").strip()
    if not city:
        return render_template("index.html", weather={"error": "Please enter a city name."}, query="")
    weather_data = fetch_weather(city)
    return render_template("index.html", weather=weather_data, query=city)


@app.route("/api/weather", methods=["GET"])
def api_weather():
    """JSON endpoint used by the JS layer when clicking a recent/favourite city."""
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "City parameter is required."}), 400
    weather_data = fetch_weather(city)
    if weather_data.get("error"):
        return jsonify(weather_data), 404
    return jsonify(weather_data)


if __name__ == "__main__":
    app.run(debug=True)
