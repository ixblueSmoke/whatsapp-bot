import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from models.nlp import detect_language, classify_intent, train_model

def test_detect_language():
    # Test for English
    assert detect_language("Hello, how are you?") == "en"
    
    # Test for Arabic
    assert detect_language("مرحبا، كيف حالك؟") == "ar"
    
    # Test for unsupported language
    assert detect_language("Bonjour, comment ça va?") == "unknown"

def test_classify_intent():
    # Retrain the model with updated TRAIN_DATA
    train_model()

    # Test for greeting intent
    assert classify_intent("Hello") == "greeting"

    # Test for help intent
    assert classify_intent("I need help") == "help"
    assert classify_intent("Can you assist me?") == "help"
    assert classify_intent("I need assistance") == "help"

    # Test for price inquiry intent
    assert classify_intent("كم سعر بديل الرخام؟") == "طلب_سعر"
    assert classify_intent("What is the price of the wood alternative?") == "طلب_سعر"

    # Test for image request intent
    assert classify_intent("أرسل لي صورة المنتج") == "طلب_صور"
    assert classify_intent("Can you send me the catalog?") == "طلب_صور"

    # Test for general inquiry intent
    assert classify_intent("وش تنصحني أختار؟") == "استفسار_عام"
    assert classify_intent("Do you offer installation services?") == "استفسار_عام"

    # Test for complaint intent
    assert classify_intent("ما عجبتني الخدمة") == "شكوى"
    assert classify_intent("I want to return the product") == "شكوى"

    # Test for fallback intent
    assert classify_intent("This is an unknown query") == "fallback"