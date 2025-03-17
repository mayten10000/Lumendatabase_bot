from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import request
import logging

logging.basicConfig(level=logging.INFO)


API_TOKEN = '7897800053:AAG0gOh2OGfsa1Cd_sV-x3fFAMjtw-qs6N8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот для работы с Lumendatabase. Прожми /check_notifications")

@dp.message(Command("check_notifications"))
async def check_notifications(message: Message):
    await message.reply("Проврка")

    notifications = await fetch_api_lumendatabase

    if notifications:
        for notice in notifications:
            await message.answer(
                f"Уведомление: {notice.get('title', 'Без названия')}\nСсылка: {notice.get('url', 'Нет ссылки')}")

    else:
        await message.reply("Уведомлений нет")

    await message.reply("Успешно")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())