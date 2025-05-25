import sqlite3
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()  # Load environment variables from .env file

DB_NAME = "employees.db"

# Twilio credentials from environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

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
            return row[0] if row else ""
    except Exception as e:
        logging.error(f"Error getting user language: {e}")
        return ""

def set_user_section(user_number: str, section: str):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE user_context SET
                    last_section = ?,
                    last_updated = ?
                WHERE user_number = ?
            ''', (section, datetime.now().isoformat(), user_number))
            conn.commit()
    except Exception as e:
        logging.error(f"Error setting user section: {e}")

def get_user_section(user_number: str) -> str:
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('SELECT last_section FROM user_context WHERE user_number = ?', (user_number,))
            row = c.fetchone()
            return row[0] if row else ""
    except Exception as e:
        logging.error(f"Error getting user section: {e}")
        return ""

# إرسال كتالوج PDF أو أي ملف وسائط عبر Twilio
def send_catalog(to_number: str, file_url: str, caption: str = ""):
    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        payload = {
            "To": f"whatsapp:{to_number}",
            "From": f"whatsapp:{twilio_whatsapp_number}",
            "Body": caption,
            "MediaUrl": file_url
        }
        response = requests.post(url, data=payload, auth=(account_sid, auth_token))
        logging.info(f"Catalog sent to {to_number}. Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending catalog to {to_number}: {e}")

# توجيه العميل لاستلام الكتالوج داخل المحادثة
def send_catalog_instruction(to_number: str):
    caption = "📎 لتحميل كتالوج المنتجات، اضغط على الرابط التالي:"
    file_url = "https://your-app-name.onrender.com/catalog.pdf"  # استبدل باسم تطبيقك على Render
    send_catalog(to_number, file_url, caption)
