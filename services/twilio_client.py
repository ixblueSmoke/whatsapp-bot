import logging
from twilio.rest import Client
from config import account_sid, auth_token, twilio_whatsapp_number

_logger = logging.getLogger(__name__)

# Single shared client
_client = Client(account_sid, auth_token)

def _to_whatsapp(number: str) -> str:
    return f"whatsapp:{number}"

def send_text(user_number: str, message: str):
    try:
        _client.messages.create(
            from_=_to_whatsapp(twilio_whatsapp_number),
            to=_to_whatsapp(user_number),
            body=message
        )
    except Exception:
        _logger.exception("send_text failed")

def send_media(user_number: str, media_url: str, caption: str = ""):
    try:
        _client.messages.create(
            from_=_to_whatsapp(twilio_whatsapp_number),
            to=_to_whatsapp(user_number),
            body=caption,
            media_url=[media_url]
        )
    except Exception:
        _logger.exception("send_media failed")

def send_template(user_number: str, template_sid: str, fallback_text: str = None):
    try:
        # If Twilio account and template support content_sid, use it.
        _client.messages.create(
            from_=_to_whatsapp(twilio_whatsapp_number),
            to=_to_whatsapp(user_number),
            content_sid=template_sid
        )
    except Exception:
        _logger.exception("send_template failed")
        if fallback_text:
            send_text(user_number, fallback_text)