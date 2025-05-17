from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import os

train_data = [
    ("كم سعر بديل الرخام؟", "طلب_سعر"),
    ("بكم الواجهة الحجرية؟", "طلب_سعر"),
    ("What is the price of the wood alternative?", "طلب_سعر"),
    ("Can you send me the price list?", "طلب_سعر"),
    ("How much does it cost?", "طلب_سعر"),
    ("I want to know the price of the product", "طلب_سعر"),
    ("How much is the delivery fee?", "طلب_سعر"),
    ("What are the prices for your products?", "طلب_سعر"),
    ("أرسل لي صورة المنتج", "طلب_صور"),
    ("أبغى كتالوج", "طلب_صور"),
    ("Can you send me the catalog?", "طلب_صور"),
    ("Do you have a product catalog?", "طلب_صور"),
    ("Send me pictures of the products", "طلب_صور"),
    ("I need product images", "طلب_صور"),
    ("Show me the available designs", "طلب_صور"),
    ("وش تنصحني أختار؟", "استفسار_عام"),
    ("هل في توصيل؟", "استفسار_عام"),
    ("I have a question about the product", "استفسار_عام"),
    ("What are the payment options?", "استفسار_عام"),
    ("Can you provide more details about the product?", "استفسار_عام"),
    ("I need assistance with my order", "استفسار_عام"),
    ("What is the warranty policy?", "استفسار_عام"),
    ("Do you offer installation services?", "استفسار_عام"),
    ("What are the available colors?", "استفسار_عام"),
    ("ما عجبتني الخدمة", "شكوى"),
    ("المنتج فيه مشكلة", "شكوى"),
    ("I have a complaint about the service", "شكوى"),
    ("I received a damaged product", "شكوى"),
    ("I want to file a complaint", "شكوى"),
    ("I want to return the product", "شكوى")
]

model_path = "nlp_intent_classifier.joblib"

def train_and_save_model():
    texts, labels = zip(*train_data)
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(texts, labels)
    joblib.dump(model, model_path)
    print(f"✅ Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()