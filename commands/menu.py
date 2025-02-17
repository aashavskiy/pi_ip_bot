# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu.py

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from commands.ip import ip_command  # Import the ip_command function
from commands.uptime import uptime_command  # Import uptime command function

# This function handles buttons pressed in the menu
async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    if update.message:
        text = update.message.text.strip()
        message = update.message
    elif update.callback_query:
        text = update.callback_query.data
        message = update.callback_query.message
    else:
        return

    context.args = text.split()

    # Check if the button pressed is "IP"
    if text == "🌐 IP":
        await ip_command(update, context)  # This will trigger the ip_command when IP button is pressed
    elif text == "⏳ Uptime":
        await uptime_command(update, context)
    else:
        await message.reply_text("❌ Unknown command. Please use the menu or type /help for available commands.")

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["🌐 IP", "⏳ Uptime"]
    ], resize_keyboard=True, one_time_keyboard=True)

async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu()  # Send the main menu only once
    )