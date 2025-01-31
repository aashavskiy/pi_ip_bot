from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

async def menu_command(update: Update, context: CallbackContext) -> None:
    """Displays an inline button menu in the chat instead of the standard Telegram menu."""
    
    keyboard = [
        [InlineKeyboardButton("📡 Get IP", callback_data="cmd_ip")],
        [InlineKeyboardButton("🕒 Time", callback_data="cmd_time"),
         InlineKeyboardButton("📊 Uptime", callback_data="cmd_uptime")],
        [InlineKeyboardButton("🌦 Weather", callback_data="cmd_weather")],
        [InlineKeyboardButton("🔑 VPN Menu", callback_data="cmd_vpn")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔽 **Choose an option:**", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    """Handles button presses from the menu."""
    query = update.callback_query
    await query.answer()

    command_mapping = {
        "cmd_ip": "/ip",
        "cmd_time": "/time",
        "cmd_uptime": "/uptime",
        "cmd_weather": "/weather",
        "cmd_vpn": "/vpn",
    }

    command = command_mapping.get(query.data)
    
    if command:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"⌛ Executing `{command}`...", parse_mode="Markdown")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=command)