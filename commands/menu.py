from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
from bot_utils import is_user_in_vpn_whitelist, is_user_authorized, request_approval
from commands.vpn.devices import add_device, list_devices, get_config, remove_device
from commands.ip import ip_command
from commands.uptime import uptime_command
import logging

# Define states for the conversation
DEVICE_NAME, REMOVE_DEVICE_NAME = range(2)

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["🌐 IP", "⏳ Uptime"],
        ["🔐 VPN"]
    ], resize_keyboard=True, one_time_keyboard=True)

def get_vpn_menu():
    return ReplyKeyboardMarkup([
        ["➕ Add Device", "📋 List Devices"],
        ["🔑 Get Config", "❌ Remove Device"],
        ["🔙 Main Menu"]
    ], resize_keyboard=True, one_time_keyboard=True)

async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        return

    await update.message.reply_text("Main Menu:", reply_markup=get_main_menu())

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    """
    Handles button presses in the main menu.
    """
    text = update.message.text

    if text == "🔐 VPN":
        await vpn_menu(update, context)
    elif text == "🌐 IP":
        await ip_command(update, context)
    elif text == "⏳ Uptime":
        await uptime_command(update, context)
    elif text == "🔙 Main Menu":
        await menu_command(update, context)
    else:
        await update.message.reply_text("Unknown command, please use the menu.")

async def vpn_menu(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("VPN Menu:", reply_markup=get_vpn_menu())

def get_conversation_handler():
    """
    Returns the conversation handler for managing menu interactions.
    """
    return ConversationHandler(
        entry_points=[CommandHandler("menu", menu_command)],
        states={
            DEVICE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_device)],
            REMOVE_DEVICE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_device)]
        },
        fallbacks=[CommandHandler("menu", menu_command)]
    )

# Register handlers
menu_handler = CommandHandler("menu", menu_command)
ip_button_handler = MessageHandler(filters.Regex("^🌐 IP$"), ip_command)
uptime_button_handler = MessageHandler(filters.Regex("^⏳ Uptime$"), uptime_command)
vpn_button_handler = MessageHandler(filters.Regex("^🔐 VPN$"), vpn_menu)
handle_menu_buttons_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_buttons)

# Add handlers to dispatcher
dispatcher.add_handler(menu_handler)
dispatcher.add_handler(handle_menu_buttons_handler)
dispatcher.add_handler(ip_button_handler)  # Fix for IP button
