import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TG_API_TOKEN')

print(API_TOKEN)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот для работы с Lumendatabase. Нажми /check_notifications")

@dp.message(Command("check_notifications"))
async def check_notifications(message: Message):
    await message.reply("Проверка уведомлений...")

    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notifications WHERE processed = 0")

    rows = cursor.fetchall()

    unanswrd_notices = [row for row in rows]

    if unanswrd_notices:
        
        for notice in unanswrd_notices:

            await message.answer(
                f"Уведомление: {notice}" # Изменить формат и добавить данные вывода 
            )
            
    conn.close()

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
