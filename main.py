from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

API_TOKEN = '7897800053:AAG0gOh2OGfsa1Cd_sV-x3fFAMjtw-qs6N8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот для работы с Lumendatabase.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())