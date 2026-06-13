import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask, request, jsonify
import requests
import threading

# Налаштування токенів
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") # Цю змінну додамо на Railway

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Посилання на ваш GitHub Pages (змінюємо хвостик для скидання кешу)
WEBAPP_URL = "https://stoyanovichbogdan.github.io/genius-telegram-bot2/?v=4"

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.json
        user_text = data.get("question", "")
        
        if not user_text:
            return jsonify({"text": "Порожній запит"}), 400
            
        # Запит до безкоштовного ШІ через Groq API (модель Llama 3)
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": user_text}]
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
        response_data = response.json()
        
        ai_text = response_data['choices'][0]['message']['content']
        return jsonify({"text": ai_text})
        
    except Exception as e:
        return jsonify({"text": f"Помилка сервера ШІ: {str(e)}"}), 500

def run_bot():
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except:
        pass
    print("🤖 Бот успішно запущений!")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
