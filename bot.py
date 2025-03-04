from aiogram import Bot, Dispatcher
from aiogram.types import Message
import os

# Загрузим токен из файла
def load_token():
    with open("token.txt", "r") as file:
        return file.read().strip()  # Убираем лишние пробелы и символы новой строки

TOKEN = load_token()  # Загружаем токен
bot = Bot(token=TOKEN)  # Создаем объект бота
dp = Dispatcher()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("Привет! Я бот, который будет с тобой общаться.")

@dp.message_handler(commands=['help'])
async def help(message: Message):
    await message.answer("Скажи что-нибудь, и я постараюсь ответить.")

@dp.message_handler()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
