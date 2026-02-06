import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PRODUCT_URLS = [
    "PASTE_SHEIN_PRODUCT_LINK_HERE"
]

bot = Bot(token=TOKEN)

def check_stock(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    return "Add to Bag" in soup.text

while True:
    for url in PRODUCT_URLS.copy():
        try:
            if check_stock(url):
                bot.send_message(
                    chat_id=CHAT_ID,
                    text="🚨 SHEIN Alert!\nYour wishlist product is BACK IN STOCK 🛍️"
                )
                PRODUCT_URLS.remove(url)
        except:
            pass
    time.sleep(900)
