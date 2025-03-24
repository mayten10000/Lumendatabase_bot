import schedule
import time

import parser
import tg_bot

import logging
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from aiocache import cached
import sqlite3

import pandas as pd
from datetime import datetime
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

def daily_check():
    parser()
    # прогон уведомлений через AI и запись ответов
    # заполнение гугл форм из ответов
    tg_bot() # вывод уведомлений (+-) и ответов (-) в тг-боте
    
schedule.every().day.at("14:15").do(daily_check)

while True:
    schedule.run_pending()  
    time.sleep(60)  
