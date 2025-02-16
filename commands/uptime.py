# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/uptime.py

import subprocess
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher

# Get the current dispatcher instance
dp = Dispatcher.get_current()

# Function to get system uptime
def get_system_uptime():
    try:
        result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error retrieving uptime: {e}"

# Handler for the UPTIME command
@dp.message_handler(Command("UPTIME"))
async def uptime_command_handler(message: Message):
    uptime_info = get_system_uptime()
    await message.reply(f"System uptime: {uptime_info}")