"""
Configuration module for WhatsApp Cloud API.
Loads environment variables and stores API settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# WhatsApp Cloud API Configuration
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = "1057654137421852"
WHATSAPP_BUSINESS_ACCOUNT_ID = "1496762318835949"
RECEIVER_NUMBER = os.getenv("RECEIVER_NUMBER")  # Set in .env or pass via command line

# API Base URL
API_VERSION = "v22.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def set_receiver_number(number):
    """Set the receiver number dynamically."""
    global RECEIVER_NUMBER
    # Remove + and spaces if present
    RECEIVER_NUMBER = number.replace("+", "").replace(" ", "").replace("-", "")
    return RECEIVER_NUMBER


# Validate configuration
def validate_config():
    """Validate that all required configuration is present."""
    if not ACCESS_TOKEN:
        raise ValueError(
            "ACCESS_TOKEN not found! Please set it in your .env file or environment variables."
        )
    if not RECEIVER_NUMBER:
        raise ValueError(
            "RECEIVER_NUMBER not found! Set it in .env file or pass as argument: python main.py <number>"
        )
    print("[CONFIG] Configuration loaded successfully.")
    print(f"[CONFIG] Receiver: {RECEIVER_NUMBER}")
    return True
