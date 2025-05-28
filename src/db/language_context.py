import sqlite3

DB_PATH = "user_lang.db"

def set_user_language(user_number, lang):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS user_lang (user TEXT PRIMARY KEY, lang TEXT)")
        c.execute("INSERT OR REPLACE INTO user_lang (user, lang) VALUES (?, ?)", (user_number, lang))
        conn.commit()

def get_user_language(user_number):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS user_lang (user TEXT PRIMARY KEY, lang TEXT)")
        c.execute("SELECT lang FROM user_lang WHERE user = ?", (user_number,))
        row = c.fetchone()
        return row[0] if row else None
