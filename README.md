# 📧 EmailPitchGenerator-Bot

A simple AI-powered cold email generator built with **Flask** and **Google Gemini API**, paired with a responsive frontend deployed via **GitHub Pages**. Ideal for automating market research and crafting effective, personalized cold emails based on real insights.

> 🌐 **Live**: [Render App](https://emailpitchgenerator-bot.onrender.com)

---

## 🚀 Features

- 🔐 Gemini API Key Validation
- 🔍 Market Research Query Generation
- 🌐 Real-time Web Search Summarization
- ✉️ Personalized Cold Email Generation
- 📋 Copy-to-Clipboard for generated email

---

## 🧾 File Structure

```
EmailPitchGenerator-Bot/
├── app.py                       # Flask app backend
├── requirements.txt             # Python dependencies
├── templates/
│   ├── base.html
│   ├── index.html
│   └── answer.html
├── static/
│   └── css/
│       └── styles.css
└── README.md
```

---

## 🛠 Setup & Run Locally

### Backend (Flask)

1. Clone the repository:
   ```bash
   git clone https://github.com/jayeshkaithwas/EmailPitchGenerator-Bot.git
   cd EmailPitchGenerator-Bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```

Backend will be running at `http://127.0.0.1:5000`.

---

## ✍️ Usage

1. Go to the [Frontend Page](https://emailpitchgenerator-bot.onrender.com)
2. Enter a target industry or company.
3. Backend will:
   - Generate market research queries
   - Perform web search on each
   - Summarize results
   - Generate a cold email using Gemini
4. Copy the email and start pitching!

---

## 🧠 Powered By

- [Google Gemini API](https://ai.google.dev)
- [Bootstrap 5](https://getbootstrap.com/)
- [Render.com](https://render.com) for backend deployment

---
