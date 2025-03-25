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
ADMIN_ID = int(os.getenv('TG_ADMIN_ID'))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.reply("Привет! Я бот для работы с Lumendatabase.")

async def send_notifications(message: Message):
    await message.reply("Проверка уведомлений...")

    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notifications WHERE processed = 0")

    rows = cursor.fetchall()

    unanswrd_notices = [row for row in rows]

    if unanswrd_notices:
        
        for notice in unanswrd_notices:

            await bot.send_message(
                ADMIN_ID,
                f"{title}\nСайт: {site}\nURL уведомления: https://lumendatabase.org/notices/{notice_id}\nОтвет из встречной формы: \n{response}\n" 
            )
            
    conn.close()

async def main():
    await send_notifications()
    await dp.start_polling(bot)

asyncio.run(main())
