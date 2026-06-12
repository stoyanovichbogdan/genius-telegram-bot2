import os
import requests
import telebot

# Беремо токен з налаштувань сервера (так безпечніше) або вставте вручну
TOKEN = os.getenv("BOT_TOKEN", "8932957182:AAFY-nyjA9uyZ6oyVBMX24O7E8dRh5uRg5Q")
bot = telebot.TeleBot(TOKEN)

# Налаштування вашого ШІ FlowiseAI
API_URL = "https://cloud.flowiseai.com/api/v1/prediction/bcbe9834-1547-4656-b4a0-d3446e14f571"


def ask_ai(question_text):
    try:
        response = requests.post(API_URL, json={"question": question_text})
        result = response.json()
        return result.get(
            "text", result.get("output", "Не вдалося отримати текст відповіді.")
        )
    except Exception as e:
        return f"Помилка ШІ: {str(e)}"


# Обробник усіх текстових повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    ai_response = ask_ai(message.text)
    bot.reply_to(message, ai_response)


if __name__ == "__main__":
    print("Бот успішно запущений в режимі Polling...")
    bot.infinity_polling()