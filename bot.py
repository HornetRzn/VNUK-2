import logging
import aiohttp
import asyncio
import os
from aiogram import Bot, Dispatcher, types

# Получаем токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен бота
API_KEY = os.getenv("DEEPINFRA_API_KEY")  # API-ключ от DeepInfra

# Проверка, если переменные окружения не заданы
if not TOKEN or not API_KEY:
    raise ValueError("Не задан один из обязательных ключей: TELEGRAM_BOT_TOKEN или DEEPINFRA_API_KEY")

# Функция общения с AI
async def chat_with_ai(user_message: str):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",  # Можно заменить модель на другую, если нужно
        "messages": [{"role": "user", "content": user_message}]
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()  # Проверка на ошибки HTTP
                data = await response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            return "Произошла ошибка при общении с AI."

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ответ на реплай
@dp.message(lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.id)
async def reply_handler(message: types.Message):
    user_text = message.text
    reply = await chat_with_ai(user_text)
    await message.reply(reply)

# Приветственное сообщение
@dp.message(lambda message: "привет" in message.text.lower())
async def greet_user(message: types.Message):
    await message.reply("Привет, псинка! Как теперь тебе?", parse_mode="Markdown")  # Используем строку вместо ParseMode

async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Очистка старых вебхуков
    await dp.start_polling()  # Запуск бота на опрос сообщений

if __name__ == "__main__":
    asyncio.run(main())
