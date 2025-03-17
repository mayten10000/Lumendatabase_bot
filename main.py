import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import request
import logging
from bs4 import BeautifulSoup
import aiohttp


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

    page_url = "https://www.lumendatabase.org/notices"

    notifications = await parser_lumen(page_url)

    if notifications:
        for notice in notifications:
            await message.answer(
                f"Уведомление: {notice.get('title', 'Без названия')}\nСсылка: {notice.get('url', 'Нет ссылки')}")

    else:
        await message.reply("Уведомлений нет")

    await message.reply("Успешно")
async def parser_lumen(page_url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(page_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    notices = []

                    # Пример парсинга (замените селекторы на реальные)
                    for item in soup.select('.notice-item'):  # Замените на реальный CSS-селектор
                        title = item.select_one('.title').text.strip() if item.select_one('.title') else "Без названия"
                        url = item.select_one('a')['href'] if item.select_one('a') else "#"
                        notices.append({
                            "title": title,
                            "url": f"https://www.lumendatabase.org{url}"
                        })

                    return notices
                else:
                    logging.error(f"Ошибка при запросе страницы: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"Ошибка при подключении к сайту: {e}")
            return []

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())