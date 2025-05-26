#language_context.py

# Simple in-memory storage for demonstration; replace with persistent storage as needed.
_user_languages = {}

def get_user_language(user_number):
    return _user_languages.get(user_number)

def set_user_language(user_number, language):
    _user_languages[user_number] = language