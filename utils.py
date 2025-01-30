import os

BOT_WHITELIST_FILE = "bot_whitelist.txt"

# Load whitelist from file
def load_whitelist(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as f:
        return {line.split("#")[0].strip() for line in f.read().splitlines()}  # ✅ Store only user IDs

# Add a user to a specific whitelist
def add_to_whitelist(user_id, username, filename):
    whitelist = load_whitelist(filename)
    whitelist.add(f"{user_id}#{username}")  # Store as `user_id#username`
    with open(filename, "w") as f:
        f.write("\n".join(whitelist))