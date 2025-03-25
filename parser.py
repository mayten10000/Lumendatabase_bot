import logging
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from aiocache import cached
import sqlite3
import csv

###########

logging.basicConfig(level=logging.INFO)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
@cached(ttl=60)
async def parser_lumen():
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            base_url = "https://lumendatabase.org/notices/"

            with open('sites.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  
                sites = [row[0] for row in reader]  
            
            notices = []  

            for site_url in sites:

                p = 1
                
                while True:
                                        
                    page_url = f'{base_url}search?page={p}&term={site_url}'
                    
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
                                    "url": url.replace('/notices/', ''),
                                    "site": site_url
                                })
                            await asyncio.sleep(2)
                        else:
                            logging.error(f"Ошибка при запросе страницы {p}: {response.status}")
                            break
                    
                    next_button = soup.select_one('span.next a[rel="next"]')

                    if not next_button:
                        print(f"Уведомления с сайта {site_url} успешно собраны")
                        break

                    p += 1

                    if p == 11: break # DEL (добавить авторизацию Lumendatabase для просмотра дальше 10-ой страницы)

            for notice in notices:
                        
                notice_url = f'https://lumendatabase.org/notices/{notice["url"]}'

                async with session.get(notice_url) as notice_page:

                    if notice_page.status == 200:
                        html = await notice_page.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        description = soup.select_one("div.row div.description span.field").get_text()

                        notice['description'] = description

                    else:
                        print('Не удалось подключится к сайту уведомления')

                    await asyncio.sleep(2)
                        
            return notices  

        except Exception as e:
            logging.error(f"Ошибка при подключении к сайту: {e}")
            return []

async def write_notices():

    notifications = await parser_lumen()

    conn = sqlite3.connect("notifications.db")
    cursor = conn.cursor()
    
    if notifications:
        
        for notice in notifications:

                site_notice = notice.get('site', 'Без сайта')
                title_notice = notice.get('title', 'Без названия')
                id_notice = notice.get('url', 'Нет идентификатора')

                
                #text_notice = f"{notice.get('title', 'Без названия')}\nСсылка на уведомление: {notice.get('url', 'Нет ссылки')}\nСсылка на сайт: {notice.get('site', 'Без сайта')}"
                
                cursor.execute("INSERT INTO notifications (site, notice_id, title) VALUES (?, ?, ?)", (site_notice, id_notice, title_notice))
                
    conn.commit()
    conn.close()

    logging.info('Все уведомления успешно собраны !')

asyncio.run(write_notices())
