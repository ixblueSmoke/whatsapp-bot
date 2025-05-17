#!/bin/bash

# security_audit.sh
# فحص أمني مبدئي لكود البوت

set -e

echo "🔐 بدء فحص الأمان..."

# 1. التأكد من وجود .env وعدم رفعه بالخطأ
if grep -qE '^\s*\.env$' .gitignore; then
  echo "✅ ملف .env مستثنى من git (آمن)"
else
  echo "❌ تحذير: .env غير مضاف لـ .gitignore"
fi

# 2. فحص أسرار حساسة داخل الكود
if grep -rE '(TWILIO|SECRET|TOKEN|PASSWORD).*=' src/*.py; then
  echo "❌ تحذير: تم العثور على متغيرات حساسة داخل الكود"
else
  echo "✅ لا يوجد أسرار مكشوفة في الكود"
fi

# 3. فحص مكتبات Python لمخاطر معروفة
if command -v pip-audit &> /dev/null; then
  pip-audit
else
  echo "ℹ️ pip-audit غير مثبت. للتثبيت: pip install pip-audit"
fi

# 4. فحص كود Python للثغرات المعروفة
if command -v bandit &> /dev/null; then
  bandit -r src
else
  echo "ℹ️ bandit غير مثبت. للتثبيت: pip install bandit"
fi

echo "✅ تم الفحص."
