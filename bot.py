import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TELEGRAM_BOT_TOKEN, DEEPINFRA_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объекта бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Асинхронная функция для общения с AI
async def chat_with_ai(user_message):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        # Асинхронный запрос с использованием aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                # Проверка на успешный ответ
                response.raise_for_status()
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    except aiohttp.ClientError as e:
        logging.error(f"Ошибка при запросе к AI: {e}")
        return "Извините, произошла ошибка при обращении к сервису."

# Обработчик для сообщений, которые являются реплаем на сообщения бота
@dp.message(lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.id)
async def reply_handler(message: types.Message):
    user_text = message.text  # Получаем текст сообщения от пользователя
    reply = await chat_with_ai(user_text)  # Получаем ответ от AI
    await message.reply(reply, parse_mode="HTML")  # Отправляем ответ в чат

# Обработчик для приветственного сообщения
@dp.message(lambda message: "привет" in message.text.lower())
async def greet_user(message: types.Message):
    await message.reply("Привет, как я могу помочь?")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
