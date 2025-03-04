import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import F
import os

# Получаем токен из переменных окружения
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Устанавливаем базовый уровень логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Простой обработчик команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я твой бот. Чем могу помочь?")

# Обработчик текстовых сообщений с использованием ключевого слова
@dp.message_handler(F.text == "Привет")
async def greet(message: Message):
    await message.answer("Привет! Как дела?")

# Основная функция для запуска бота
if __name__ == '__main__':
    import asyncio

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
