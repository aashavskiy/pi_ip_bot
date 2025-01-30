import os

BOT_WHITELIST_FILE = "bot_whitelist.txt"
VPN_WHITELIST_FILE = "vpn_whitelist.txt"

# Load a whitelist from a file
def load_whitelist(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as f:
        return set(f.read().splitlines())

# Add a user to a specific whitelist
def add_to_whitelist(user_id, username, filename):
    whitelist = load_whitelist(filename)
    whitelist.add(f"{user_id}#{username}")  # Store as `user_id#username`
    with open(filename, "w") as f:
        f.write("\n".join(whitelist))