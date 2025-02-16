# File: commands/ip.py

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from commands.ip import ip_command

async def ip_button_handler(update: Update, context: CallbackContext) -> None:
    """
    Handles the IP button press
    """
    await ip_command(update, context)

# Register handler
ip_handler = MessageHandler(filters.Regex("^🌐 IP$"), ip_button_handler)