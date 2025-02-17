# /Users/alexanderashavskiy/projects/pi_ip_bot/piipbot.py

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from commands.menu import menu_command, handle_menu_commands
from commands.router_menu import handle_router_commands

# Initialize bot
app = Application.builder().token("YOUR_BOT_TOKEN").build()

# Register handlers
app.add_handler(CommandHandler("menu", menu_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_commands))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_router_commands))

print("🤖 Bot is running...")
app.run_polling()