from decouple import config, UndefinedValueError
import logging
import sys

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

REQUIRED_ENV_VARS = [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_WHATSAPP_NUMBER",
    "YOUR_WHATSAPP_NUMBER"
]

def get_env_var(key):
    try:
        value = config(key)
        if not value:
            raise ValueError
        return value
    except (UndefinedValueError, ValueError):
        logging.error(f"\u274c Environment variable '{key}' is missing or empty.")
        sys.exit(f"\u274c Please set '{key}' in your .env file or system environment.")

account_sid = get_env_var("TWILIO_ACCOUNT_SID")
auth_token = get_env_var("TWILIO_AUTH_TOKEN")
twilio_whatsapp_number = get_env_var("TWILIO_WHATSAPP_NUMBER")
your_whatsapp_number = get_env_var("YOUR_WHATSAPP_NUMBER")
debug_mode = config("DEBUG", default="False").lower() == "true"