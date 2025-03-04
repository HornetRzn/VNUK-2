import logging
import requests
import asyncio
import os
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("8124475955:AAGfEaT9CuzUhitVUKK6oIl3rE3HSWesw3E")  # Токен бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
API_KEY = os.getenv("NmtzgEazVU6yGONQVcGPByw5SbWWykkQ")  # API-ключ от DeepInfra

# Функция общения с AI
async def chat_with_ai(user_message):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ответ только на реплай
@dp.message(lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.id)
async def reply_handler(message: types.Message):
    user_text = message.text
    reply = await chat_with_ai(user_text)
    await message.reply(reply)

# Ключевые слова
@dp.message(lambda message: "привет" in message.text.lower())
async def greet_user(message: types.Message):
    await message.reply("Привет, псинка! Как теперь тебе?")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
