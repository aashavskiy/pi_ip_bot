import os

BOT_WHITELIST_FILE = "bot_whitelist.txt"
VPN_WHITELIST_FILE = "vpn_whitelist.txt"

# Load bot and VPN whitelists
def load_whitelist(filename):
    """Load a whitelist from a file."""
    if not os.path.exists(filename):
        return {}

    with open(filename, "r") as file:
        return dict(line.strip().split(" ", 1) for line in file if line.strip())

BOT_WHITELIST = load_whitelist(BOT_WHITELIST_FILE)
VPN_WHITELIST = load_whitelist(VPN_WHITELIST_FILE)

# Add user to a whitelist
def add_to_whitelist(user_id, username, filename):
    """Add a user to a specific whitelist file."""
    with open(filename, "a") as file:
        file.write(f"{user_id} {username}\n")

def add_to_bot_whitelist(user_id, username):
    """Add a user to the bot whitelist."""
    add_to_whitelist(user_id, username, BOT_WHITELIST_FILE)

def add_to_vpn_whitelist(user_id, username):
    """Add a user to the VPN whitelist."""
    add_to_whitelist(user_id, username, VPN_WHITELIST_FILE)