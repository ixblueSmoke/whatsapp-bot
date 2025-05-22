import logging
from flask import request
from flask import jsonify
from models.nlp import detect_language, classify_intent
from models.responses import get_response
from models.context import update_user_intent, get_last_intent
from twilio.twiml.messaging_response import MessagingResponse

def bot(request):
    try:
        from_number = request.values.get('From', '')
        incoming_message = request.values.get('Body', '').strip()

        # تحديد اللغة
        lang = detect_language(incoming_message)

        # تصنيف النية الحالية
        intent = classify_intent(incoming_message)
        logging.info(f"Detected intent: {intent} from: {from_number}")

        # استرجاع آخر نية محفوظة
        last_intent = get_last_intent(from_number)

        # تحديث السياق بالنية الحالية
        update_user_intent(from_number, intent)

        # توليد الرد بناء على النية الحالية والسياق السابق
        base_response = get_response(intent, lang)
        if last_intent and last_intent != intent:
            followup = {
                "ar": f" (سابقًا سألت عن: {last_intent})",
                "en": f" (previously you asked about: {last_intent})"
            }[lang]
            base_response += followup

        return jsonify({"message": base_response})

    except Exception as e:
        logging.error(f"Error in bot handler: {e}")
        resp = MessagingResponse()
        resp.message("حدث خطأ ما! (Something went wrong)")
        return str(resp)
