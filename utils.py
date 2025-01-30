import os

WHITELIST_FILE = "whitelist.txt"

def load_whitelist(filename=WHITELIST_FILE):
    """ Load the whitelist from a file. """
    if not os.path.exists(filename):
        return set()
    
    with open(filename, "r") as file:
        return set(line.strip().split()[0] for line in file if line.strip())

def check_whitelist(user_id):
    """ Check if a user is in the whitelist. """
    whitelist = load_whitelist()
    return str(user_id) in whitelist