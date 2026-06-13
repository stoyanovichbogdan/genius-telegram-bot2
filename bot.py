import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Бот бере токен з Variables на Railway
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

if not TELEGRAM_TOKEN:
    print("❌ Помилка: ТОКЕН НЕ ЗНАЙДЕНО! Перевірте вкладку Variables на Railway.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- ОЦЕЙ БЛОК ВИРІШИТЬ ПОМИЛКУ 409 КОНФЛІКТУ ---
try:
    print("🧹 Очищення старих сесій та вебхуків Telegram...")
    bot.delete_webhook(drop_pending_updates=True)
    print("✅ Сесію успішно очищено!")
except Exception as e:
    print(f"⚠️ Попередження під час очищення: {e}")
# ------------------------------------------------

# Ваше посилання на готовий WebApp сайт
WEBAPP_URL = "https://stoyanovichbogdan.github.io/genius-telegram-bot2/?v=2"

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = InlineKeyboardMarkup()
    
    # Кнопка для відкриття вашого гарного вікна
    webapp_button = InlineKeyboardButton(
        text="🚀 Відкрити ШІ-Вікно", 
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_button)
    
    welcome_text = (
        "👋 Привіт!\n"
        "Натисни кнопку нижче, щоб відкрити окреме вікно додатка де будеш розмовляти з ШІ.\n"
    )
    
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        reply_markup=markup
    )

# Запуск бота
print("🤖 Бот із підтримкою WebApp успішно запущений на Railway!")
bot.infinity_polling()
