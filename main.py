import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from aiocache import cached


# Настройки
logging.basicConfig(level=logging.INFO)

API_TOKEN = '7897800053:AAG0gOh2OGfsa1Cd_sV-x3fFAMjtw-qs6N8'  # Замените на ваш токен

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот для работы с Lumendatabase. Нажми /check_notifications")

@dp.message(Command("check_notifications"))

async def check_notifications(message: Message):
    await message.reply("Проверка уведомлений...")

    notifications = await parser_lumen()
    if notifications:
        for notice in notifications:
            await message.answer(
                f"Уведомление: {notice.get('title', 'Без названия')}\nСсылка: {notice.get('url', 'Нет ссылки')}"
            )
    else:
        await message.reply("Уведомлений нет")

    await message.reply("Успешно")


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
@cached(ttl=60)
async def parser_lumen():
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            base_url = "https://lumendatabase.org/notices/search?"
            site_url = "&term=youtube.com&sort_by="

            notices = []  

            p = 1
            while True:  
                page_url = base_url + f'page={p}' + site_url
                print(f"Парсинг {p}-ой страницы: {page_url}")

                async with session.get(page_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        for item in soup.select('li.notice.result'):  
                            title = item.select_one('h3.title a').text.strip() if item.select_one('.title') else "Без названия"
                            url = item.select_one('a')['href'] if item.select_one('a') else "#"
                            notices.append({
                                "title": title,
                                "url": f"https://www.lumendatabase.org{url}"  
                            })
                        await asyncio.sleep(2)
                    else:
                        logging.error(f"Ошибка при запросе страницы {p}: {response.status}")
                        break
                    
                next_button = soup.select_one('span.next a[rel="next"]')
                if not next_button:
                    print("Страницы для парсинга закончились")
                    break

                p += 1

            return notices  

        except Exception as e:
            logging.error(f"Ошибка при подключении к сайту: {e}")
            return []

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
