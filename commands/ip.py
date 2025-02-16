# commands/ip.py

from telegram import Update
from telegram.ext import CallbackContext

def ip_command(update: Update, context: CallbackContext):
    update.message.reply_text("IP command executed.")

def ip_button_handler(update: Update, context: CallbackContext):
    update.message.reply_text("IP button pressed.")