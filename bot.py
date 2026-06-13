import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN", "8932957182:AAFY-nyjA9uyZ6oyVBMX24O7E8dRh5uRg5Q")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Посилання на ваш завантажений HTML-сайт
WEBAPP_URL = "https://ТВОЄ_ІМЯ.github.io/назва_репозиторію/" 

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = InlineKeyboardMarkup()
    
    # Створюємо спеціальну кнопку WebApp
    webapp_button = InlineKeyboardButton(
        text="🚀 Відкрити ШІ-Вікно", 
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_button)
    
    bot.send_message(
        message.chat.id, 
        "Привіт! Натисни кнопку нижче, щоб відкрити окреме вікно додатка з налаштуваннями дизайну:", 
        reply_markup=markup
    )

print("Бот WebApp запущений...")
bot.infinity_polling()
