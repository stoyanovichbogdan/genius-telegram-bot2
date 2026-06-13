import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Отримуємо токен з налаштувань Railway
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Посилання на ваш GitHub Pages (змінюємо цифру v=5, щоб Telegram точно оновив кеш сайту)
WEBAPP_URL = "https://stoyanovichbogdan.github.io/genius-telegram-bot2/?v=5"

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
        "Натисни кнопку нижче, щоб відкрити ШІ"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

if __name__ == "__main__":
    # Очищаємо застряглі вебхуки, якщо вони були
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except:
        pass
        
    print("🤖 Бот успішно запущений без зайвих модулів!")
    bot.infinity_polling()
