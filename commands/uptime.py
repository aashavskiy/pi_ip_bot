import subprocess
from telegram import Update
from telegram.ext import CallbackContext
from logger import log_request

async def uptime_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    await log_request(user_id, username, "/uptime")  # ✅ Now passing all required arguments

    try:
        # Get system uptime
        uptime_output = subprocess.check_output("uptime -p", shell=True).decode().strip()
        await update.message.reply_text(f"⏳ Server Uptime: `{uptime_output}`", parse_mode="Markdown")

    except subprocess.CalledProcessError as e:
        await update.message.reply_text("❌ Error: Unable to fetch system uptime.")
        print(f"ERROR: Failed to fetch uptime - {e}")  # Log the error