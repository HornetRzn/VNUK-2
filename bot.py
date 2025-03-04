import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"

# Бесплатный AI (Llama 2)
async def chat_with_ai(user_message):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": "Bearer БЕСПЛАТНЫЙ_API_КЛЮЧ"}
    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Отвечает только на реплай
@dp.message_handler(lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.id)
async def reply_handler(message: types.Message):
    user_text = message.text
    reply = await chat_with_ai(user_text)
    await message.reply(reply)

# Ключевые слова
@dp.message_handler(lambda message: "привет" in message.text.lower())
async def greet_user(message: types.Message):
    await message.reply("Привет! Как твои дела?")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
