from telegram import Update
from telegram.ext import CallbackContext
from utils import add_to_whitelist, load_whitelist

VPN_WHITELIST_FILE = "vpn_whitelist.txt"

async def handle_vpn_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split("_")
    action = callback_data[1]
    user_id = callback_data[2]
    username = callback_data[3] if action == "approve" else None

    if action == "approve":
        add_to_whitelist(user_id, username, VPN_WHITELIST_FILE)

        # ✅ Reload whitelist dynamically
        global VPN_WHITELIST
        VPN_WHITELIST = load_whitelist(VPN_WHITELIST_FILE)

        await query.edit_message_text(f"✅ User @{username} ({user_id}) has been approved for VPN access.")
        await context.bot.send_message(chat_id=user_id, text="🎉 You have been approved for VPN access! Use /menu to see VPN commands.")
    else:
        await query.edit_message_text(f"❌ User {user_id} was denied VPN access.")