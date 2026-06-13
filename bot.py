import os
import requests
import telebot

# ================= НАЛАШТУВАННЯ =================
# Бот спочатку шукає токен у змінних Railway, якщо ні — бере ваш текст
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN", "ТУТ_ТВІЙ_ТОКЕН_ЯКЩО_НЕ_ЧЕРЕЗ_VARIABLES")

FLOWISE_API_URL = "https://cloud.flowiseai.com/api/v1/prediction/bcbe9834-1547-4656-b4a0-d3446e14f571"
# ================================================

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Множина (set) для збереження ID користувачів, які натиснули /start
activated_users = set()


# Обробник команди /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    chat_id = message.chat.id
    # Додаємо користувача в список активованих
    activated_users.add(chat_id)

    welcome_text = (
        "👋 Привіт! Я твій асистент зі штучним інтелектом.\n"
        "Тепер ми знайомі! Можеш ставити мені будь-які запитання, і я відповім."
    )
    bot.send_message(chat_id, welcome_text)


# Обробник усіх інших текстових повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    chat_id = message.chat.id

    # Перевіряємо, чи користувач активував бота через /start
    if chat_id not in activated_users:
        error_text = "❌ Помилка! Будь ласка, спочатку напишіть або натисніть /start, щоб розпочати діалог."
        bot.send_message(chat_id, error_text)
        return  # Зупиняємо виконання функції, далі код не йде

    # --- Якщо користувач активований, працюємо з Flowise як зазвичай ---

    # Показуємо статус "друкує...", щоб користувач бачив, що бот думає
    bot.send_chat_action(chat_id, "typing")

    # Формуємо запит для Flowise
    payload = {
        "question": user_text,
        "overrideConfig": {
            "sessionId": str(chat_id),  # Пам'ять для кожного окремо
        },
    }

    try:
        # Відправляємо повідомлення до Flowise
        response = requests.post(FLOWISE_API_URL, json=payload)
        response.raise_for_status()

        response_data = response.json()

        # Витягуємо текст відповіді
        bot_reply = response_data.get(
            "text", response_data.get("output", "Вибач, не зміг знайти відповідь.")
        )

        # Надсилаємо відповідь користувачу в Telegram
        bot.send_message(chat_id, bot_reply)

    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту до Flowise: {e}")
        bot.send_message(
            chat_id,
            "Ой, мій мозок (Flowise) зараз недоступний. Спробуй трохи пізніше!",
        )
    except Exception as e:
        print(f"Невідома помилка: {e}")
        bot.send_message(
            chat_id, "Щось пішло не так під час обробки повідомлення."
        )


# Запускаємо бота
print("🤖 Бот успішно запущений! Напиши йому в Telegram.")
bot.infinity_polling()
