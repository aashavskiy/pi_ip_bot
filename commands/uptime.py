# File: commands/uptime.py

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from commands.uptime import uptime_command

async def uptime_button_handler(update: Update, context: CallbackContext) -> None:
    """
    Handles the Uptime button press
    """
    await uptime_command(update, context)

# Register handler
uptime_handler = MessageHandler(filters.Regex("^⏳ Uptime$"), uptime_button_handler)