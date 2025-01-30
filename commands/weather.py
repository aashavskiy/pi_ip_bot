import requests
from telegram import Update
from telegram.ext import CallbackContext
from logger import log_request

async def weather_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    await log_request(user_id, username, "/weather")  # ✅ Now passing all required arguments

    try:
        # Get weather data from Open-Meteo API
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast?latitude=32.1848&longitude=34.8713&current_weather=true"
        )
        response.raise_for_status()
        data = response.json()

        temperature = data["current_weather"]["temperature"]
        weather_message = f"🌤 Current temperature in Raanana: {temperature}°C"

        await update.message.reply_text(weather_message)

    except requests.RequestException as e:
        await update.message.reply_text("❌ Error: Unable to fetch the weather data.")
        print(f"ERROR: Failed to fetch weather - {e}")  # Log the error