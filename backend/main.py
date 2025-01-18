from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Middleware to handle CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENWEATHER_API_KEY = "api_key"

# Updated playlists for combined categories
WEATHER_PLAYLISTS = {
    "clear": [
        "",
        "",
        "",
    ],
    "cloudy_rainy": [
        "",
        "",
        "",
    ],
    "snowy_misty": [
        "",
        "",
        "",
    ],
}

# Function to map OpenWeather API's weather to simplified categories
def map_weather_to_category(weather_main):
    weather_main = weather_main.lower()
    if weather_main in ["clear"]:
        return "clear"
    elif weather_main in ["clouds", "rain", "drizzle", "thunderstorm"]:
        return "cloudy_rainy"
    elif weather_main in ["snow", "mist", "fog", "haze", "dust", "sand", "squall", "tornado"]:
        return "snowy_misty"
    else:
        return "clear"  # Default fallback category

@app.get("/weather")
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_main = data["weather"][0]["main"]
        category = map_weather_to_category(weather_main)
        playlists = WEATHER_PLAYLISTS.get(category, WEATHER_PLAYLISTS["clear"])
        return {"weather": weather_main, "category": category, "playlists": playlists}
    else:
        return {"error": "City not found or API error."}
