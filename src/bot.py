import logging
import atexit
from flask import send_from_directory
# Third-party imports
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler

# Local imports
from config import (
    account_sid, auth_token, twilio_whatsapp_number,
    your_whatsapp_number, debug_mode
)
from handlers.handlers import bot
from db.db import init_db
from reminders.reminders import send_reminder

# Initialize Flask app
app = Flask(__name__)

# Rate limiting setup
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

# Twilio client setup
client = Client(account_sid, auth_token)

# Register routes
@app.route("/webhook", methods=["POST"])
@limiter.limit("5 per minute")
def bot_route():
    try:
        return bot(request)
    except Exception as e:
        logging.error(f"Error in bot route: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Background scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder, 'interval', hours=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route("/catalog.pdf")
def serve_catalog():
    return send_from_directory("static", "catalog.pdf")


# Application entry point
if __name__ == "__main__":
    logging.info("Initializing database...")
    init_db()
    logging.info("Starting Flask server...")
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
