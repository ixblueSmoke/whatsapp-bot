# 🤖 WhatsApp Business Bot

Bot for handling customer inquiries via WhatsApp using Twilio API

## 🚀 Features
- Intent classification (Arabic/English)
- Automated responses
- Employee escalation
- Conversation logging
- Scheduled reminders

## 📦 Project Structure
```bash
whatsapp-bot/
├── src/
│   ├── core/          # Core configurations
│   ├── db/            # Database operations
│   ├── handlers/      # Message processing
│   ├── models/        # ML models
│   ├── services/      # External services
│   └── utils/         # Helper functions
└── tests/             # All test suites
```

## 🛠 Setup
1. Clone repo:
```bash
git clone https://github.com/ixbluesmoke/whatsapp-bot.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Fill your Twilio credentials
```

4. Train NLP model:
```bash
python src/models/train_model.py
```

## ⚙️ Configuration
| Variable                | Description                          |
|-------------------------|--------------------------------------|
| `TWILIO_ACCOUNT_SID`    | Twilio account SID                   |
| `TWILIO_AUTH_TOKEN`     | Twilio authentication token          |
| `TWILIO_PHONE_NUMBER`   | Your Twilio WhatsApp number          |

## 🧪 Testing
```bash
# Run all tests
pytest tests/

# Test specific module
pytest tests/unit/test_handlers.py -v
```

## 🌐 Deployment
**Render.com:**
```yaml
# render.yaml
services:
  - type: web
    name: whatsapp-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/bot.py
```

## 📄 Documentation
- [Twilio API Docs](https://www.twilio.com/docs/whatsapp/api)
- [Bot Flowchart](docs/FLOW.md)

## 🤝 Contribution
1. Fork the project
2. Create your feature branch
3. Submit a PR

## 📜 License
MIT