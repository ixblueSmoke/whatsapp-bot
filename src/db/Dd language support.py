import sqlite3
import logging
from datetime import datetime
import requests
from config import account_sid, auth_token, twilio_whatsapp_number

DB_NAME = "employees.db"

TWILIO_API_URL = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

def init_db():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()

            # جدول الموظفين
            c.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE
                )
            ''')

            # جدول السياق للمستخدم
            c.execute('''
                CREATE TABLE IF NOT EXISTS user_context (
                    user_number TEXT PRIMARY KEY,
                    last_intent TEXT,
                    last_updated TEXT,
                    language TEXT,
                    last_section TEXT
                )
            ''')

            conn.commit()
            logging.info("Database tables created or verified.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

def set_user_language(user_number: str, lang: str):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO user_context (user_number, language, last_updated)
                VALUES (?, ?, ?)
                ON CONFLICT(user_number) DO UPDATE SET
                    language = excluded.language,
                    last_updated = excluded.last_updated
            ''', (user_number, lang, datetime.now().isoformat()))
            conn.commit()
    except Exception as e:
        logging.error(f"Error setting user language: {e}")

def get_user_language(user_number: str) -> str:
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('SELECT language FROM user_context WHERE user_number = ?', (user_number,))
            row = c.fetchone()
            return row[0] if row and row[0] is not None else ""
    except Exception as e:
        logging.error(f"Error getting user language: {e}")
        return ""

def set_user_section(user_number: str, section: str):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            # Ensure the user exists before updating
            c.execute('SELECT 1 FROM user_context WHERE user_number = ?', (user_number,))
            if c.fetchone():
                c.execute('''
                    UPDATE user_context SET
                        last_section = ?,
                        last_updated = ?
                    WHERE user_number = ?
                ''', (section, datetime.now().isoformat(), user_number))
            else:
                c.execute('''
                    INSERT INTO user_context (user_number, last_section, last_updated)
                    VALUES (?, ?, ?)
                ''', (user_number, section, datetime.now().isoformat()))
            conn.commit()
    except Exception as e:
        logging.error(f"Error setting user section: {e}")

def get_user_section(user_number: str) -> str:
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('SELECT last_section FROM user_context WHERE user_number = ?', (user_number,))
            row = c.fetchone()
            return row[0] if row and row[0] is not None else ""
    except Exception as e:
        logging.error(f"Error getting user section: {e}")
        return ""

# إرسال كتالوج PDF أو أي ملف وسائط عبر Twilio
def send_catalog(to_number: str, file_url: str, caption: str = ""):
    try:
        payload = {
            "To": f"whatsapp:{to_number}",
            "From": f"whatsapp:{twilio_whatsapp_number}",
            "Body": caption,
            "MediaUrl": file_url
        }
        response = requests.post(TWILIO_API_URL, data=payload, auth=(account_sid, auth_token))
        logging.info(f"Catalog sent to {to_number}. Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending catalog to {to_number}: {e}")

# إرسال صورة
def send_image(to_number: str, image_url: str, caption: str = ""):
    try:
        payload = {
            "To": f"whatsapp:{to_number}",
            "From": f"whatsapp:{twilio_whatsapp_number}",
            "Body": caption,
            "MediaUrl": image_url
        }
        response = requests.post(TWILIO_API_URL, data=payload, auth=(account_sid, auth_token))
        logging.info(f"Image sent to {to_number}. Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending image to {to_number}: {e}")

# إرسال نص ثابت (مثلاً قائمة الفروع)
def send_text_reply(to_number: str, text: str):
    try:
        payload = {
            "To": f"whatsapp:{to_number}",
            "From": f"whatsapp:{twilio_whatsapp_number}",
            "Body": text
        }
        response = requests.post(TWILIO_API_URL, data=payload, auth=(account_sid, auth_token))
        logging.info(f"Text reply sent to {to_number}. Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending text reply to {to_number}: {e}")

# إرسال خيارات منتجات بعد اختيار القسم
def send_product_options(to_number: str, lang: str = "ar"):
    try:
        if lang == "ar":
            text = "🧱 اختر نوع المنتج:\n1. رخام أبيض مقاس 60×60\n2. جرانيت رمادي مقاس 80×80"
        else:
            text = "🧱 Choose a product type:\n1. White Marble 60×60\n2. Grey Granite 80×80"
        send_text_reply(to_number, text)
    except Exception as e:
        logging.error(f"Error sending product options: {e}")

# ردود بناءً على الزر المضغوط
def handle_quick_reply_button(button_id: str, user_number: str):
    if button_id == "ar_catalog":
        send_catalog_instruction(user_number)
    elif button_id == "en_catalog":
        send_catalog_instruction(user_number, lang="en")
    elif button_id in ["ar_branches", "en_branches"]:
        text = "📍 الفروع: الرياض - جدة - الدمام" if "ar" in button_id else "📍 Branches: Riyadh, Jeddah, Dammam"
        send_text_reply(user_number, text)
    elif button_id in ["ar_support", "en_support"]:
        text = "☎️ للتواصل مع الدعم: 9200XXXXXX" if "ar" in button_id else "☎️ Contact support at: +9669200XXXXXX"
        send_text_reply(user_number, text)
    elif button_id in ["ar_projects", "en_projects"]:
        caption = "🖼️ بعض من أعمالنا السابقة:" if "ar" in button_id else "🖼️ Some of our past projects:"
        send_image(user_number, "https://your-app-name.onrender.com/static/img1.jpg", caption)
        send_image(user_number, "https://your-app-name.onrender.com/static/img2.jpg")
        send_image(user_number, "https://your-app-name.onrender.com/static/img3.jpg")
    elif button_id in ["ar_products", "en_products"]:
        lang = "ar" if "ar" in button_id else "en"
        send_product_options(user_number, lang)

# توجيه العميل لاستلام الكتالوج داخل المحادثة
def send_catalog_instruction(to_number: str, lang: str = "ar"):
    caption = "📎 لتحميل كتالوج المنتجات، اضغط على الرابط التالي:" if lang == "ar" else "📎 Click the link to download our product catalog:"
    file_url = "https://your-app-name.onrender.com/catalog.pdf"  # استبدل باسم تطبيقك على Render
    send_catalog(to_number, file_url, caption)
