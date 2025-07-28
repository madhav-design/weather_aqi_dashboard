from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
AQICN_API_KEY = os.getenv("AQICN_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    data = {}
    if request.method == "POST":
        city = request.form["city"]

        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        weather_response = requests.get(weather_url).json()

        aqi_url = f"https://api.waqi.info/feed/{city}/?token={AQICN_API_KEY}"
        aqi_response = requests.get(aqi_url).json()

        if weather_response.get("cod") == 200 and aqi_response.get("status") == "ok":
            data = {
                "city": city.title(),
                "temperature": weather_response["main"]["temp"],
                "humidity": weather_response["main"]["humidity"],
                "wind": weather_response["wind"]["speed"],
                "aqi": aqi_response["data"]["aqi"],
                "pm25": aqi_response["data"]["iaqi"].get("pm25", {}).get("v", "N/A"),
                "pm10": aqi_response["data"]["iaqi"].get("pm10", {}).get("v", "N/A"),
                "lat": weather_response["coord"]["lat"],
                "lon": weather_response["coord"]["lon"]
            }
        else:
            data["error"] = "City not found or API error. Please try again."

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
