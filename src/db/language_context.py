# db/language_context.py
user_lang_store = {}

def set_user_language(user_number, lang):
    user_lang_store[user_number] = lang

def get_user_language(user_number):
    return user_lang_store.get(user_number)
