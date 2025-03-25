import schedule
import time

import parser
import ai_handler # пока не встроен в общий процесс
import filler_g_forms # пока не встроен в общий процесс
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
    # ai_handler() # прогон уведомлений через AI 
    # filler_g_forms() # заполнение гугл форм из ответов
    tg_bot() # вывод уведомлений (+-) и ответов (-) в тг-боте
    
schedule.every().day.at("14:15").do(daily_check)

while True:
    schedule.run_pending()  
    time.sleep(60)  
