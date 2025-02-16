# File: piipbot.py

from telegram.ext import ApplicationBuilder
from commands.menu import menu_command, get_main_menu, get_conversation_handler
from commands.buttons import handle_menu_buttons
from commands.ip import ip_button_handler
from commands.vpn import vpn_button_handler
from commands.uptime import uptime_button_handler

# Initialize application
application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

# Register handlers
application.add_handler(menu_command)
application.add_handler(handle_menu_buttons)
application.add_handler(ip_button_handler)
application.add_handler(vpn_button_handler)
application.add_handler(uptime_button_handler)

# Start bot
if __name__ == "__main__":
    application.run_polling()