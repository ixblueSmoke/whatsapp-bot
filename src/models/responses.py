RESPONSES = {
    "طلب_سعر": {
        "ar": "🧾 الأسعار تبدأ من 120 ريال حسب نوع المنتج. أخبرني ما المنتج الذي ترغب به.",
        "en": "🧾 Prices start from 120 SAR depending on the product."
    },
    "طلب_صور": {
        "ar": "📸 تفضل كتالوج المنتجات: https://yourdomain.com/catalog",
        "en": "📸 Here's our product catalog: https://yourdomain.com/catalog"
    },
    "استفسار_عام": {
        "ar": "👋 يسعدني مساعدتك! هل تود معرفة الأسعار، التوصيل، أو نوع المنتجات؟",
        "en": "👋 Happy to help! Would you like info on prices, delivery, or product types?"
    },
    "شكوى": {
        "ar": "📣 نأسف لسماع ذلك. سيقوم موظف خدمة العملاء بالتواصل معك قريبًا.",
        "en": "📣 Sorry to hear that. A customer service representative will contact you shortly."
    },
    "افتراضي": {
        "ar": "❓ لم أفهم استفسارك. هل يمكنك إعادة صياغته؟",
        "en": "❓ I didn't understand your request. Could you rephrase?"
    }
}

def get_response(intent: str, lang: str = "ar") -> str:
    if intent in RESPONSES:
        return RESPONSES[intent].get(lang, RESPONSES[intent]["ar"])
    return RESPONSES["افتراضي"].get(lang, RESPONSES["افتراضي"]["ar"])
