import os
import requests
import telebot
from flask import Flask, request, jsonify
from flask_cors import CORS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Налаштування Telegram бота
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Посилання на твій сайт
WEBAPP_URL = "https://stoyanovichbogdan.github.io/genius-telegram-bot2/?v=6"

# Налаштування Flask (сервера-посередника)
app = Flask(__name__)
CORS(app)  # Дозволяємо сайту звертатися до сервера без помилок CORS

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = InlineKeyboardMarkup()
    webapp_button = InlineKeyboardButton(text="🚀 Відкрити ШІ-Вікно", web_app=WebAppInfo(url=WEBAPP_URL))
    markup.add(webapp_button)
    
    welcome_text = "👋 Привіт! Натисни кнопку нижче, щоб відкрити безпечний ШІ-чат ✨"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# API-endpoint для нашого сайту index.html
@app.route('/api/chat', models=['POST']) # або просто methods=['POST']
@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    data = request.json
    user_query = data.get("question")
    conv_id = data.get("conversation_id", "")
    user_id = data.get("user_id", "default_user")

    dify_key = os.getenv("DIFY_API_KEY")
    
    if not dify_key:
        return jsonify({"text": "Помилка: На Railway не налаштовано DIFY_API_KEY"}), 500

    # Безпечно відправляємо запит з сервера Railway на Dify
    try:
        response = requests.post(
            "https://api.dify.ai/v1/chat-messages",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {dify_key}"
            },
            json={
                "inputs": {},
                "query": user_query,
                "response_mode": "blocking",
                "conversation_id": conv_id,
                "user": f"tg_webapp_{user_id}"
            },
            timeout=30
        )
        dify_data = response.json()
        return jsonify({
            "text": dify_data.get("answer", "Немає відповіді від Dify"),
            "conversation_id": dify_data.get("conversation_id", "")
        })
    except Exception as e:
        return jsonify({"text": f"Помилка сервера: {str(e)}"}), 500

if __name__ == "__main__":
    # Запускаємо бота у фоні, щоб він не заважав Flask серверу
    import threading
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except:
        pass
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    
    # Запускаємо веб-сервер на порті, який видасть Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
