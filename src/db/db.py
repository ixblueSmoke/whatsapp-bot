import sqlite3

# Initialize the database connection
def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE
        )
    ''')
    # Add this block to create user_context table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_context (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL UNIQUE,
            context TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add a new employee
def add_employee(name, phone):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, phone)
        VALUES (?, ?)
    ''', (name, phone))
    conn.commit()
    conn.close()

# Ensure employees table exists (for compatibility with your bot.py)
def ensure_employees_db():
    init_db()
