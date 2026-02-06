import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

TRACK_FILE = "products.txt"

def load_products():
    if not os.path.exists(TRACK_FILE):
        return set()
    with open(TRACK_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_products(products):
    with open(TRACK_FILE, "w") as f:
        for p in products:
            f.write(p + "\n")

products = load_products()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😌 Hi babe!\n\n"
        "Main SHEIN stock watcher hoon 👀🛍️\n\n"
        "Commands:\n"
        "/add <product link> ➕\n"
        "/remove <product link> ❌\n"
        "/list 📋\n\n"
        "Jab bhi stock aayega, main ping kar dungi 🤭💖"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Link bhi bhejo na cutie 😅")
        return

    url = context.args[0]
    products.add(url)
    save_products(products)

    await update.message.reply_text("📝 Added!\nIs product pe nazar rakhungi 👀💕

")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Kaunsa remove karu? Link bhejo 😅")
        return

    url = context.args[0]
    if url in products:
        products.remove(url)
        save_products(products)
        await update.message.reply_text("❌ Removed!\nAb isko track nahi kar rahi 😌")
    else:
        await update.message.reply_text("Ye product list me tha hi nahi 🤷‍♀️")

async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not products:
        await update.message.reply_text("Abhi koi product track nahi ho raha 😴")
        return

    msg = "📋 *Tracking products:*\n\n"
    for i, p in enumerate(products, 1):
        msg += f"{i}. {p}\n"

    await update.message.reply_text(msg)

def check_stock():
    for url in list(products):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")

            if "Out of Stock" not in soup.text:
                app.bot.send_message(
                    chat_id=CHAT_ID,
                    text=(
                        "😍 *OMG BABE!*\n"
                        "Tumhari wishlist ka product *BACK IN STOCK* hai 🛍️🔥\n\n"
                        f"🔗 {url}\n\n"
                        "Jaldi jao warna phir sold out 😏"
                    ),
                    parse_mode="Markdown"
                )
                products.remove(url)
                save_products(products)
        except:
            pass

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("list", list_products))

scheduler = BackgroundScheduler()
scheduler.add_job(check_stock, "interval", minutes=15)
scheduler.start()

app.run_polling()
