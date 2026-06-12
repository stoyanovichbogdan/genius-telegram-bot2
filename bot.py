import telebot
import requests

# ================= НАЛАШТУВАННЯ =================
# Встав сюди свій токен від BotFather
TELEGRAM_TOKEN = '8932957182:AAFY-nyjA9uyZ6oyVBMX24O7E8dRh5uRg5Q'

# Встав сюди URL свого Flowise (з вікна API Endpoint)
FLOWISE_API_URL = "https://cloud.flowiseai.com/api/v1/prediction/bcbe9834-1547-4656-b4a0-d3446e14f571"
# ================================================

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    chat_id = message.chat.id
    
    # Показуємо статус "друкує...", щоб користувач бачив, що бот думає
    bot.send_chat_action(chat_id, 'typing')
    
    # Формуємо запит для Flowise
    payload = {
        "question": user_text,
        # sessionId передає унікальний ID чату, щоб пам'ять працювала для кожного користувача окремо
        "overrideConfig": {
            "sessionId": str(chat_id) 
        }
    }
    
    try:
        # Відправляємо повідомлення до Flowise
        response = requests.post(FLOWISE_API_URL, json=payload)
        response.raise_for_status() # Перевіряємо, чи немає помилок HTTP
        
        response_data = response.json()
        
        # Витягуємо текст відповіді
        bot_reply = response_data.get('text', 'Вибач, я не зміг згенерувати відповідь.')
        
        # Надсилаємо відповідь користувачу в Telegram
        bot.send_message(chat_id, bot_reply)
        
    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту до Flowise: {e}")
        bot.send_message(chat_id, "Ой, мій мозок (Flowise) зараз недоступний. Перевір, чи він запущений!")
    except Exception as e:
        print(f"Невідома помилка: {e}")
        bot.send_message(chat_id, "Щось пішло не так під час обробки повідомлення.")

# Запускаємо бота
print("🤖 Бот успішно запущений! Напиши йому в Telegram.")
bot.infinity_polling()
