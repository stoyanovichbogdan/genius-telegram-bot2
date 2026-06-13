import os
import requests
import telebot
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# 1. Налаштування Telegram бота
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Посилання на твій сайт на GitHub Pages
WEBAPP_URL = "https://stoyanovichbogdan.github.io/genius-telegram-bot2/?v=6"

# 2. Налаштування Flask сервера-посередника
app = Flask(__name__)
CORS(app)  # Дозволяємо сайту звертатися до сервера без помилок CORS

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = InlineKeyboardMarkup()
    webapp_button = InlineKeyboardButton(
        text="🚀 Відкрити ШІ-Вікно", 
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_button)
    
    welcome_text = (
        "👋 Привіт!\n"
        "Натисни кнопку нижче, щоб відкрити безпечний ШІ-чат з анімацією зірки! ✨\n"
        "Тепер історія зберігається, а ввід блокується, поки ШІ думає."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# 3. API-endpoint для нашого сайту index.html
@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    data = request.json
    user_query = data.get("question")
    conv_id = data.get("conversation_id", "")
    user_id = data.get("user_id", "default_user")

    dify_key = os.getenv("DIFY_API_KEY")
    
    if not dify_key:
        return jsonify({"text": "Помилка: На Railway не налаштовано змінну DIFY_API_KEY"}), 500

    # Безпечно відправляємо запит з сервера Railway на Dify.ai
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
        return jsonify({"text": f"Помилка сервера Railway: {str(e)}"}), 500

if __name__ == "__main__":
    # Очищаємо застряглі вебхуки, якщо вони були
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except:
        pass
        
    # Запускаємо Telegram-бота в окремому потоці (фоні), щоб він не заважав Flask
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    print("🤖 Telegram бот успішно запущений у фоні!")
    
    # Запускаємо вебсервер Flask на порті, який виділить Railway (за замовчуванням 5000)
    port = int(os.environ.get("PORT", 5000))
    print(f"🌍 Сервер Flask стартує на порті {port}...")
    app.run(host="0.0.0.0", port=port)
