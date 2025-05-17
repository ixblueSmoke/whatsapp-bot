import os
import joblib
import logging
from langdetect import detect
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

MODEL_PATH = "nlp_intent_classifier.joblib"

# Sample data for training fallback if no model exists
TRAIN_DATA = [
    ("كم سعر بديل الرخام؟", "طلب_سعر"),
    ("بكم الواجهة الحجرية؟", "طلب_سعر"),
    ("What is the price of the wood alternative?", "طلب_سعر"),
    ("أرسل لي صورة المنتج", "طلب_صور"),
    ("Can you send me the catalog?", "طلب_صور"),
    ("وش تنصحني أختار؟", "استفسار_عام"),
    ("Do you offer installation services?", "استفسار_عام"),
    ("ما عجبتني الخدمة", "شكوى"),
    ("I want to return the product", "شكوى")
]

def detect_language(text: str) -> str:
    try:
        # Define language-specific keywords
        language_keywords = {
            "en": ["hello", "hi", "please"],
            "ar": ["مرحبا", "السلام", "ابغى"]
        }

        # Check for keywords in the text
        for lang, keywords in language_keywords.items():
            if any(word in text for word in keywords):
                return lang

        # Fallback to langdetect
        return detect(text)
    except Exception as e:
        logging.warning(f"Language detection failed: {str(e)}")
        return "ar"

def train_model():
    try:
        texts, labels = zip(*TRAIN_DATA)
        model = make_pipeline(CountVectorizer(), MultinomialNB())
        model.fit(texts, labels)
        joblib.dump(model, MODEL_PATH)
        logging.info("Model trained and saved successfully.")
        return model
    except Exception as e:
        logging.error(f"Error during model training: {str(e)}")
        raise

def load_or_train_model():
    try:
        if os.path.exists(MODEL_PATH):
            logging.info("Loading existing model...")
            return joblib.load(MODEL_PATH)
        else:
            logging.info("Model not found, training a new one...")
            return train_model()
    except Exception as e:
        logging.error(f"Error loading or training model: {str(e)}")
        raise

# Load on import
intent_model = load_or_train_model()

def classify_intent(text: str) -> str:
    try:
        return intent_model.predict([text])[0]
    except Exception as e:
        logging.error(f"Intent classification error: {str(e)}")
        return "fallback"  # Default fallback intent
