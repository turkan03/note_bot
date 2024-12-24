import os 
from dotenv import load_dotenv
import logging 
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging modules help know when (and why) things don't work as expected
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level = logging.INFO
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = "I'm a bot, please talk to me!"
  )

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

application.run_polling()