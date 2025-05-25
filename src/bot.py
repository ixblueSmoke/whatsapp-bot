from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import atexit

from config import account_sid, auth_token, twilio_whatsapp_number, your_whatsapp_number, debug_mode
from reminders.reminders import send_reminder
from handlers.handlers_guided import handle_quick_reply_button

app = Flask(__name__)

limiter = Limiter(app, key_func=get_remote_address, default_limits=["10 per minute"])  # Fixed Limiter usage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

@app.route("/webhook", methods=["POST"])
@limiter.limit("5 per minute")
def bot_route():
    try:
        data = request.form
        button_id = data.get("ButtonPayload")
        user_number = data.get("From", "").replace("whatsapp:", "")

        if button_id:
            handle_quick_reply_button(button_id, user_number)
            return jsonify({"status": "button handled"}), 200
        else:
            return jsonify({"message": "No button detected"}), 200

    except Exception as e:
        logging.error(f"Error in bot route: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Route for serving static files like catalog or project images
@app.route('/static/<path:filename>')  # Fixed: <filename> to <path:filename> for subfolders
def serve_static_file(filename):
    return send_from_directory('static', filename)

scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder, 'interval', hours=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def init_db():
    raise NotImplementedError

if __name__ == "__main__":
    init_db()
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
