import logging
import json
import requests
from flask import request, Response , Request
from config import account_sid, auth_token, twilio_whatsapp_number
from db.db import init_db
from db.language_context import set_user_language, get_user_language


TWILIO_API_URL = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"


def bot(req: Request):
    try:
        from_number = req.values.get('From', '').replace('whatsapp:', '')
        msg_body = req.values.get('Body', '').strip().lower()

        # تعامل مع الرد من زر (ID) بدل body لو توفر
        payload = req.form
        button_id = payload.get("ButtonReply.Id")

        # STEP 1: بدء المحادثة
        if msg_body in ["hi", "hello", "مرحبا"]:
            send_language_buttons(from_number)
            return Response(status=200)

        # STEP 2: اختيار اللغة
        if button_id == "lang_ar":
            set_user_language(from_number, "ar")
            send_section_buttons(from_number, lang="ar")
            return Response(status=200)
        elif button_id == "lang_en":
            set_user_language(from_number, "en")
            send_section_buttons(from_number, lang="en")
            return Response(status=200)

        # STEP 3: اختيار القسم
        if button_id in ["ar_prices", "en_prices"]:
            send_whatsapp_message(from_number, "الأسعار تبدأ من 100 ريال." if "ar" in button_id else "Prices start from 100 SAR.")
            return Response(status=200)

        if button_id in ["ar_branches", "en_branches"]:
            send_whatsapp_message(from_number, "فروعنا: الرياض، جدة، الدمام." if "ar" in button_id else "Our branches: Riyadh, Jeddah, Dammam.")
            return Response(status=200)

        if button_id in ["ar_support", "en_support"]:
            send_whatsapp_message(from_number, "سيتواصل معك الدعم قريبًا." if "ar" in button_id else "Support will contact you shortly.")
            return Response(status=200)

        # fallback: رجوع للقائمة الرئيسية
        if msg_body in ["رجوع", "back"]:
            lang = get_user_language(from_number) or "ar"
            send_language_buttons(from_number)
            return Response(status=200)

        # إذا مافهم شيء، يرجع للقائمة الأساسية
        send_language_buttons(from_number)
        return Response(status=200)

    except Exception as e:
        logging.error(f"Bot error: {e}")
        return Response("Internal error", status=500)


def send_whatsapp_message(to: str, text: str):
    requests.post(
        TWILIO_API_URL,
        data={
            "To": f"whatsapp:{to}",
            "From": f"whatsapp:{twilio_whatsapp_number}",
            "Body": text
        },
        auth=(account_sid, auth_token)
    )


def send_language_buttons(to: str):
    payload = {
        "To": f"whatsapp:{to}",
        "From": f"whatsapp:{twilio_whatsapp_number}",
        "ContentType": "application/json",
        "Body": json.dumps({
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": "اختر اللغة / Choose your language:"},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "lang_ar", "title": "العربية"}},
                        {"type": "reply", "reply": {"id": "lang_en", "title": "English"}}
                    ]
                }
            }
        })
    }
    requests.post(TWILIO_API_URL, data=payload, auth=(account_sid, auth_token))


def send_section_buttons(to: str, lang="ar"):
    if lang == "ar":
        text = "اختر الخدمة:"
        buttons = [
            {"type": "reply", "reply": {"id": "ar_prices", "title": "الأسعار"}},
            {"type": "reply", "reply": {"id": "ar_branches", "title": "الفروع"}},
            {"type": "reply", "reply": {"id": "ar_support", "title": "الدعم"}}
        ]
    else:
        text = "Choose a service:"
        buttons = [
            {"type": "reply", "reply": {"id": "en_prices", "title": "Prices"}},
            {"type": "reply", "reply": {"id": "en_branches", "title": "Branches"}},
            {"type": "reply", "reply": {"id": "en_support", "title": "Support"}}
        ]

    payload = {
        "To": f"whatsapp:{to}",
        "From": f"whatsapp:{twilio_whatsapp_number}",
        "ContentType": "application/json",
        "Body": json.dumps({
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": buttons}
            }
        })
    }
    requests.post(TWILIO_API_URL, data=payload, auth=(account_sid, auth_token))
