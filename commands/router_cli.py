# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_cli.py

import os
import paramiko
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Router SSH credentials from .env
ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_SSH_USER = os.getenv("ROUTER_SSH_USER")
ROUTER_SSH_PASSWORD = os.getenv("ROUTER_SSH_PASSWORD")

def run_router_command(command):
    """Execute a CLI command on the router via SSH."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ROUTER_IP, username=ROUTER_SSH_USER, password=ROUTER_SSH_PASSWORD, timeout=5)

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        client.close()

        return output if output else error
    except Exception as e:
        return f"❌ Error connecting to router: {e}"