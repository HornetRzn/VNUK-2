import logging
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Загрузка токенов
from config import TELEGRAM_BOT_TOKEN, DEEPINFRA_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Функция общения с AI через DeepInfra
async def chat_with_ai(user_message):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Реагирование на реплай
@dp.message(lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.id)
async def reply_handler(message: types.Message):
    user_text = message.text
    reply = await chat_with_ai(user_text)
    await message.reply(reply)

# Реагирование на ключевые слова
@dp.message(lambda message: "привет" in message.text.lower())
async def greet_user(message: types.Message):
    await message.reply("Привет, как я могу помочь?")

async def on_start():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
