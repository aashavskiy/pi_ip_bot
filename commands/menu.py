# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.ip import ip_command
from commands.uptime import uptime_command

# Function to handle menu button presses
async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        text = update.callback_query.data  # Handle inline button press
        await update.callback_query.answer()  # Acknowledge button press
    else:
        return

    # Match button presses with commands
    if text == "ip":
        await ip_command(update, context)
    elif text == "uptime":
        await uptime_command(update, context)
    else:
        await update.callback_query.message.reply_text("❌ Unknown command.")

# Function to generate inline keyboard menu
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🌐 IP", callback_data="ip")],
        [InlineKeyboardButton("⏳ Uptime", callback_data="uptime")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Command to display the menu
async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu()
    )