from telegram import Update
from telegram.ext import CallbackContext
from bot_utils import add_to_vpn_whitelist

async def handle_vpn_approval(update: Update, context: CallbackContext) -> None:
    """Handles admin approval or denial of VPN requests."""
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split("_")
    action = callback_data[1]
    user_id = callback_data[2]
    username = callback_data[3] if action == "approve" else None

    if action == "approve":
        add_to_vpn_whitelist(user_id, username)
        await query.edit_message_text(f"✅ User @{username} ({user_id}) has been approved for VPN access.")
        await context.bot.send_message(chat_id=user_id, text="🎉 You have been approved for VPN access! Use /adddevice to generate a configuration.")
    else:
        await query.edit_message_text(f"❌ User {user_id} was denied VPN access.")