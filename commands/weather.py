import requests
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu  # Import menu function

# Coordinates of Raanana
LATITUDE = 32.1845
LONGITUDE = 34.8707

# Function to get the weather from Open-Meteo
def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true&temperature_unit=celsius&wind_speed_unit=ms"

    try:
        response = requests.get(url)
        data = response.json()

        if "current_weather" not in data:
            return "Error: Unable to fetch weather data."

        temp = data["current_weather"]["temperature"]
        wind_speed = data["current_weather"]["windspeed"]
        weather_desc = data["current_weather"]["weathercode"]

        # Weather description mapping (simplified)
        weather_map = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤",
            2: "Partly cloudy ⛅️",
            3: "Overcast ☁️",
            45: "Fog 🌫",
            48: "Rime fog ❄️",
            51: "Light drizzle 🌦",
            53: "Moderate drizzle 🌧",
            55: "Dense drizzle 🌧",
            61: "Light rain 🌦",
            63: "Moderate rain 🌧",
            65: "Heavy rain 🌧🌧",
            71: "Light snow 🌨",
            73: "Moderate snow 🌨",
            75: "Heavy snow ❄️❄️",
            80: "Rain showers 🌦",
            81: "Heavy rain showers 🌧🌧",
            82: "Violent rain showers 🌪",
            95: "Thunderstorm ⛈",
            96: "Thunderstorm with hail ⛈❄️",
            99: "Severe thunderstorm with hail 🌩❄️"
        }

        weather_text = weather_map.get(weather_desc, "Unknown weather condition")

        return f"🌤 Weather in Raanana:\nTemperature: {temp}°C\nCondition: {weather_text}\nWind Speed: {wind_speed} m/s"

    except Exception as e:
        return f"Error retrieving weather data: {e}"

# Command handler for /weather
async def weather_command(update: Update, context: CallbackContext) -> None:
    weather_info = get_weather()
    reply_markup = get_main_menu()  # Keep the menu visible
    await update.message.reply_text(weather_info, reply_markup=reply_markup)