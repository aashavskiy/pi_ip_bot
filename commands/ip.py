# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/ip.py

import subprocess
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

# Create a router instance
router = Router()

# Function to get the external IP address
def get_external_ip():
    try:
        result = subprocess.run(["curl", "-s", "https://api.ipify.org"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error retrieving IP: {e}"

# Handler for the IP command
@router.message(Command("IP"))
async def ip_button_handler(message: Message):
    ip_address = get_external_ip()
    await message.reply(f"Your external IP: {ip_address}")