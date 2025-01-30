import os

BOT_WHITELIST_FILE = "bot_whitelist.txt"
VPN_WHITELIST_FILE = "vpn_whitelist.txt"

def load_whitelist(filename=BOT_WHITELIST_FILE):
    """ Load the whitelist from a file. """
    if not os.path.exists(filename):
        return set()
    
    with open(filename, "r") as file:
        return set(line.strip().split()[0] for line in file if line.strip())

def add_to_whitelist(user_id, username, filename=BOT_WHITELIST_FILE):
    """ Add a user to the whitelist. """
    if not os.path.exists(filename):
        open(filename, "w").close()  # Create file if missing
    
    with open(filename, "a") as file:
        file.write(f"{user_id} # {username}\n")
    
    print(f"✅ DEBUG: Added user {user_id} ({username}) to {filename}")

def check_whitelist(user_id):
    """ Check if a user is in the bot whitelist. """
    whitelist = load_whitelist()
    print(f"🔍 DEBUG: Checking bot whitelist - Loaded users: {whitelist}")  # Debug print
    return str(user_id) in whitelist