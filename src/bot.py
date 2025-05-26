from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import atexit
from twilio.rest import Client

from config import account_sid, auth_token, twilio_whatsapp_number, your_whatsapp_number, debug_mode
from db.db import init_db
from db.language_context import get_user_language, set_user_language  # You need to implement these

app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

def send_catalog(user_number, file_url, caption):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        body=caption,
        media_url=[file_url]
    )

def send_language_selection(user_number):
    text = "Please choose your language:\n1. العربية\n2. English"
    send_text_reply(user_number)

def send_language_selection_template(user_number):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        content_sid='HX0d7a28a83f0ea0b36d480970c11bc977'  # Your language selection template SID
    )

def send_template(user_number, template_sid):
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        content_sid=template_sid
    )

@app.route("/webhook", methods=["POST"])
@limiter.limit("5 per minute")
def bot_route():
    try:
        data = request.form
        button_id = data.get("ButtonPayload")
        user_number = data.get("From", "").replace("whatsapp:", "")
        incoming_text = data.get("Body", "").strip()

        # 1. Check if we know the user's language
        user_lang = get_user_language(user_number)
        if not user_lang:
            if button_id == "lang_ar":
                set_user_language(user_number, "ar")
                send_template(user_number, "HXb6ab46f20992895ce301faed42d813ec")  # Main Arabic template
                return jsonify({"status": "language set"}), 200
            elif button_id == "lang_en":
                set_user_language(user_number, "en")
                send_template(user_number, "HX1740c1806e8e58a8dbea6215db62def1")  # Main English template
                return jsonify({"status": "language set"}), 200
            else:
                send_language_selection_template(user_number)
                return jsonify({"status": "ask language"}), 200

        if button_id:
            # Language selection
            if button_id == "lang_ar":
                set_user_language(user_number, "ar")
                send_template(user_number, "HXb6ab46f20992895ce301faed42d813ec")  # Arabic main menu template
                return jsonify({"status": "language set"}), 200
            elif button_id == "lang_en":
                set_user_language(user_number, "en")
                send_template(user_number, "HX1740c1806e8e58a8dbea6215db62def1")  # English main menu template
                return jsonify({"status": "language set"}), 200

            # Catalogs menu
            elif button_id == "catalog_ar":
                send_template(user_number, "HXad63fa26ead4384c954e19572027a72b")  # Arabic catalogs template
                return jsonify({"status": "catalogs sent"}), 200
            elif button_id == "catalog_en":
                send_template(user_number, "HXcfcc075b1f58ed102944c571beb068c0")  # English catalogs template
                return jsonify({"status": "catalogs sent"}), 200

            # Branches info
            elif button_id == "branch_ar":
                send_text_reply(user_number, "📍 الفروع: الرياض - جدة - الدمام")
                return jsonify({"status": "branches sent"}), 200
            elif button_id == "branch_en":
                send_text_reply(user_number, "📍 Branches: Riyadh, Jeddah, Dammam")
                return jsonify({"status": "branches sent"}), 200

            # Support info (same for both, or customize)
            elif button_id == "support_ar":
                send_text_reply(user_number, "☎️ للتواصل مع الدعم: 9200XXXXXX\n☎️ For support: +9669200XXXXXX")
                return jsonify({"status": "support sent"}), 200
            elif button_id == "support_en":
                send_text_reply(user_number, "☎️ For support: +9669200XXXXXX")
                return jsonify({"status": "support sent"}), 200

            # Arabic main catalogs (ar_catalogs)
            if button_id == "marbele_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/SMA_Marble.pdf", "📎 كتالوج بديل الرخام")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "chipboard_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/Chipboard_cat.pdf", "📎 كتالوج بديل الخشب")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "3D_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/Private_Sma_Cat.pdf", "📎 كتالوج الطباعة ثلاثية الأبعاد")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "rizen_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/R_SMA.pdf", "📎 كتالوج الريزين")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "more_catalogs_ar":
                send_template(user_number, "HX9f5f20bb8ef61d23d9b32afe1a242e90")  # Arabic more template
                return jsonify({"status": "more catalogs sent"}), 200

            # Arabic more catalogs (ar_more)
            elif button_id == "pu_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/PU_stone.pdf", "📎 كتالوج بديل الحجر PU")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "match_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/OB_SMA.pdf", "📎 كتالوج الأوبن بوك")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "profile_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/profile_cat.pdf", "📎 كتالوج البروفايل")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "fallback_ar":
                send_template(user_number, "HXad63fa26ead4384c954e19572027a72b")  # Back to catalogs
                return jsonify({"status": "back to catalogs"}), 200

            # English main catalogs (en_catalogs)
            elif button_id == "marbele_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_marble.pdf", "📎 Marble Catalog")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "chipboard_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_wood.pdf", "📎 Wood Catalog")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "profile_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_profile.pdf", "📎 Profile Catalog")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "rizen_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_resin.pdf", "📎 Resin Catalog")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "more_en":
                send_template(user_number, "HX6842017435eb051255d2c21dd1471e64")  # English more template
                return jsonify({"status": "more catalogs sent"}), 200

            # English more catalogs (en_more)
            elif button_id == "pu_stone":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_pustone.pdf", "📎 PU Stone Catalog")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "match_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_openbook.pdf", "📎 Open Book Catalog")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "3D_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_3dprint.pdf", "📎 3D Printer Catalog")
                return jsonify({"status": "catalog sent , back to main"}), 200
            elif button_id == "fallback_en":
                send_template(user_number, "HXcfcc075b1f58ed102944c571beb068c0")  # Back to catalogs
                return jsonify({"status": "back to catalogs"}), 200

            return jsonify({"status": "button handled"}), 200
        else:
            return jsonify({"message": "No button detected"}), 200

    except Exception as e:
        logging.error(f"Error in bot route: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/static/<path:filename>')
def serve_static_file(filename):
    return send_from_directory('static', filename)

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def send_text_reply(user_number, message):
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        body=message
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
