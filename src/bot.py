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
    client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        body=caption,
        media_url=[file_url]
    )

def send_language_selection_template(user_number):
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        content_sid='HX0d7a28a83f0ea0b36d480970c11bc977'
    )

def send_template(user_number, template_sid):
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        content_sid=template_sid
    )

def send_text_reply(user_number, message):
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + user_number,
        body=message
    )

def return_to_main_menu(user_number):
    lang = get_user_language(user_number)
    if lang == "ar":
        send_template(user_number, "HXad63fa26ead4384c954e19572027a72b")
    else:
        send_template(user_number, "HXcfcc075b1f58ed102944c571beb068c0")

@app.route("/webhook", methods=["POST"])
@limiter.limit("5 per minute")
def bot_route():
    try:
        data = request.form
        button_id = data.get("ButtonPayload")
        user_number = data.get("From", "").replace("whatsapp:", "")
        incoming_text = data.get("Body", "").strip()
        user_lang = get_user_language(user_number)

        if not user_lang:
            if button_id == "lang_ar":
                set_user_language(user_number, "ar")
                send_template(user_number, "HXb6ab46f20992895ce301faed42d813ec")
                return jsonify({"status": "language set"}), 200
            elif button_id == "lang_en":
                set_user_language(user_number, "en")
                send_template(user_number, "HX1740c1806e8e58a8dbea6215db62def1")
                return jsonify({"status": "language set"}), 200
            else:
                send_language_selection_template(user_number)
                return jsonify({"status": "ask language"}), 200

        if button_id:
            if button_id == "lang_ar":
                set_user_language(user_number, "ar")
                send_template(user_number, "HXb6ab46f20992895ce301faed42d813ec")
                return jsonify({"status": "language set"}), 200
            elif button_id == "lang_en":
                set_user_language(user_number, "en")
                send_template(user_number, "HX1740c1806e8e58a8dbea6215db62def1")
                return jsonify({"status": "language set"}), 200

            elif button_id == "catalog_ar":
                send_template(user_number, "HXad63fa26ead4384c954e19572027a72b")
                return jsonify({"status": "catalogs sent"}), 200
            elif button_id == "catalog_en":
                send_template(user_number, "HXcfcc075b1f58ed102944c571beb068c0")
                return jsonify({"status": "catalogs sent"}), 200

            elif button_id == "branch_ar":
                send_text_reply(user_number, "📍 الفروع: الرياض - جدة - الدمام")
                return jsonify({"status": "branches sent"}), 200
            elif button_id == "branch_en":
                send_text_reply(user_number, "📍 Branches: Riyadh, Jeddah, Dammam")
                return jsonify({"status": "branches sent"}), 200

            elif button_id == "support_ar":
                send_text_reply(user_number, "☎️ للتواصل مع الدعم: 9200XXXXXX\n☎️ For support: +9669200XXXXXX")
                return jsonify({"status": "support sent"}), 200
            elif button_id == "support_en":
                send_text_reply(user_number, "☎️ For support: +9669200XXXXXX")
                return jsonify({"status": "support sent"}), 200

            # Arabic catalogs
            elif button_id == "marbele_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/SMA_Marble.pdf", "📎 كتالوج بديل الرخام")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "chipboard_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/Chipboard_cat.pdf", "📎 كتالوج بديل الخشب")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "3D_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/Private_Sma_Cat.pdf", "📎 كتالوج الطباعة ثلاثية الأبعاد")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "rizen_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/R_SMA.pdf", "📎 كتالوج الريزين")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "more_catalogs_ar":
                send_template(user_number, "HX9f5f20bb8ef61d23d9b32afe1a242e90")
                return jsonify({"status": "more catalogs sent"}), 200
            elif button_id == "pu_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/PU_stone.pdf", "📎 كتالوج بديل الحجر PU")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "match_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/OB_SMA.pdf", "📎 كتالوج الأوبن بوك")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "profile_ar":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/profile_cat.pdf", "📎 كتالوج البروفايل")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200

            # English catalogs
            elif button_id == "marbele_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_marble.pdf", "📎 Marble Catalog")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "chipboard_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_wood.pdf", "📎 Wood Catalog")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "profile_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_profile.pdf", "📎 Profile Catalog")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "rizen_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_resin.pdf", "📎 Resin Catalog")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "more_en":
                send_template(user_number, "HX6842017435eb051255d2c21dd1471e64")
                return jsonify({"status": "more catalogs sent"}), 200
            elif button_id == "pu_stone":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_pustone.pdf", "📎 PU Stone Catalog")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "match_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_openbook.pdf", "📎 Open Book Catalog")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200
            elif button_id == "3D_en":
                send_catalog(user_number, "https://whatsapp-bot-t7o1.onrender.com/static/catalog_3dprint.pdf", "📎 3D Printer Catalog")
                return_to_main_menu(user_number)
                return jsonify({"status": "catalog sent"}), 200

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

if __name__ == "__main__":
    init_db()
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
