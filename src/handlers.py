import os 
from dotenv import load_dotenv
import logging 
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import mydb

# Logging modules help know when (and why) things don't work as expected
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level = logging.INFO
)
# Load environment variables
load_dotenv()
# Get the Telegram bot token from the .env file
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# Create the bot application
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build() # type: ignore


# Creat function for /start commant 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id_name = update.effective_user.id # type: ignore
  user_first_name = update.effective_user.first_name # type: ignore # Get the user's first name
  mydb.user_value(user_id_name)
    
  await context.bot.send_message(
    chat_id = update.effective_chat.id, # type: ignore
    text = f"Hello {user_first_name}! 👋\nI'm your personal note assistant. Here's what I can help you with:\n\n📝 *Create a New Note*\nSend me anything you'd like to save as a note, and I'll store it for you.\n\n🔍 *Search Your Notes*\nYou can browse by categories or search through your save notes.\n\n Choose an option:\n1️⃣ Type /create to starting creat new note.\n2️⃣ Use /categories to explore and search existing notes.\n\n💡 Tip: Organize your notes into categories to find them easily later!"
  )

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

application.run_polling()