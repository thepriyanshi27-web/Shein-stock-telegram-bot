import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

URLS = [
    "https://sheinindia.onelink.me/ZrSt/5vpryx5e"
]

def check_stock():
    for url in URLS:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        if "Out of Stock" not in soup.text:
            bot.send_message(chat_id=CHAT_ID, text=f"🔥 Stock available!\n{url}")

scheduler = BlockingScheduler()
scheduler.add_job(check_stock, "interval", minutes=15)
scheduler.start()
