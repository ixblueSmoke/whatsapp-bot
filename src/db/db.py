import sqlite3
import logging

DB_NAME = 'employees.db'

# Initialize the database with all required tables
def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Table for storing employees
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE
            )
        ''')

        # Table for storing user context
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL UNIQUE,
                context TEXT
            )
        ''')

        conn.commit()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
    finally:
        conn.close()

# Optional: Add a new employee (used somewhere else maybe)
def add_employee(name, phone):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (name, phone)
            VALUES (?, ?)
        ''', (name, phone))
        conn.commit()
        logging.info(f"Employee {name} added.")
    except sqlite3.IntegrityError:
        logging.warning("Employee already exists.")
    except Exception as e:
        logging.error(f"Failed to add employee: {e}")
    finally:
        conn.close()
