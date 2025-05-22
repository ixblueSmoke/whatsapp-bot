import sqlite3
import logging
from datetime import datetime

# قاعدة البيانات
DB_NAME = "employees.db"

# إنشاء الجداول المطلوبة
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

            # جدول السياق (context)
            c.execute('''
                CREATE TABLE IF NOT EXISTS user_context (
                    user_number TEXT PRIMARY KEY,
                    last_intent TEXT,
                    last_updated TEXT
                )
            ''')

            conn.commit()
            logging.info("Database tables (employees & user_context) checked/created.")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")

# إضافة موظف جديد
def add_employee(name, phone):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO employees (name, phone)
                VALUES (?, ?)
            ''', (name, phone))
            conn.commit()
    except Exception as e:
        logging.error(f"Error adding employee: {e}")

# تحديث نية المستخدم (intent)
def update_user_intent(user_number: str, intent: str):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO user_context (user_number, last_intent, last_updated)
                VALUES (?, ?, ?)
                ON CONFLICT(user_number) DO UPDATE SET
                    last_intent = excluded.last_intent,
                    last_updated = excluded.last_updated
            ''', (user_number, intent, datetime.now().isoformat()))
            conn.commit()
    except Exception as e:
        logging.error(f"Error updating user context: {e}")

# استرجاع آخر نية للمستخدم
def get_last_intent(user_number: str) -> str:
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('SELECT last_intent FROM user_context WHERE user_number = ?', (user_number,))
            row = c.fetchone()
            return row[0] if row else ""
    except Exception as e:
        logging.error(f"Error retrieving user context: {e}")
        return ""
