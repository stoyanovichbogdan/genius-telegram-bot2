import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Бот автоматично візьме токен із налаштувань (Variables) на Railway.
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

if not TELEGRAM_TOKEN:
    print("❌ Помилка: ТОКЕН НЕ ЗНАЙДЕНО! Перевірте вкладку Variables на Railway.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ⚠️ ВСТАВТЕ СЮДИ ВАШЕ ПОСИЛАННЯ, ЯКЕ ВИЙШЛО ПІСЛЯ УКЛЮЧЕННЯ GITHUB PAGES
# Приклад: "https://bogdan25.github.io/genius-bot/"
WEBAPP_URL = "https://ТВОЄ_ІМЯ_НА_GITHUB.github.io/НАЗВА_РЕПОЗИТОРІЮ/"

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = InlineKeyboardMarkup()
    
    # Створюємо спеціальну кнопку WebApp для відкриття нашого вікна
    webapp_button = InlineKeyboardButton(
        text="🚀 Відкрити ШІ-Вікно", 
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_button)
    
    welcome_text = (
        "👋 Привіт!\n"
        "Натисни кнопку нижче, щоб відкрити окреме вікно додатка.\n"
        "Там ти зможеш змінювати тему (світла/темна), розгортати екран та спілкуватися з ШІ!"
    )
    
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        reply_markup=markup
    )

# Запуск бота
print("🤖 Бот із підтримкою WebApp успішно запущений на Railway!")
bot.infinity_polling()
