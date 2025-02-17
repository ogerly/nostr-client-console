# utils/validator.py
import re

def validate_username(username: str) -> bool:
    pattern = r"^[a-zA-Z0-9_-]{3,32}$"
    return bool(re.match(pattern, username))

def validate_relay_url(url: str) -> bool:
    return url.startswith("wss://") or url.startswith("ws://")