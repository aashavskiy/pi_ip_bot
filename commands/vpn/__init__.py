# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/vpn/__init__.py

# Delay import to avoid circular import issues
def get_vpn_router():
    from .vpn import router
    return router

__all__ = ["get_vpn_router"]