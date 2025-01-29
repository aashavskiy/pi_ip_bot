import requests
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu  # Import menu function
from logger import log_request  # Import logging function

# Function to get the weather
def get_weather():
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=32.1845&longitude=34.8707&current_weather=true&temperature_unit=celsius&wind_speed_unit=ms")
        data = response.json()

        if "current_weather" not in data:
            return "Error: Unable to fetch weather data."

        temp = data["current_weather"]["temperature"]
        wind_speed = data["current_weather"]["windspeed"]
        return f"🌤 Weather in Raanana:\nTemperature: {temp}°C\nWind Speed: {wind_speed} m/s"

    except Exception as e:
        return f"Error retrieving weather data: {e}"

# Command handler for /weather
async def weather_command(update: Update, context: CallbackContext) -> None:
    await log_request(update)  # Log the request
    weather_info = get_weather()
    reply_markup = get_main_menu()
    await update.message.reply_text(weather_info, reply_markup=reply_markup)