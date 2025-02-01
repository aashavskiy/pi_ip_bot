import subprocess
from telegram import Update
from telegram.ext import CallbackContext
from utils import is_user_authorized, request_approval
from logger import log_request

async def uptime_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await log_request(user_id, username, "/uptime")

    try:
        # Get system uptime
        uptime_output = subprocess.check_output("uptime -p", shell=True).decode().strip()
        await update.message.reply_text(f"⏳ Server Uptime: `{uptime_output}`", parse_mode="Markdown")

    except subprocess.CalledProcessError as e:
        await update.message.reply_text("❌ Error: Unable to fetch system uptime.")
        print(f"ERROR: Failed to fetch uptime - {e}")  # Log the error