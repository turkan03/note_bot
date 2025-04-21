import os 
from dotenv import load_dotenv
import logging 
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler,MessageHandler, ConversationHandler, filters
import mydb

# Logging modules help know when (and why) things don't work as expected
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level = logging.INFO
)

# Load environment variables
load_dotenv()
# Get the Telegram bot token from the .env file
TELEGRAM_KEY = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_KEY:
  raise ValueError("TELEGRAM_TOKEN not found in .env file or environment variables")
# Create the bot application
application = Application.builder().token(TELEGRAM_KEY).build() # type: ignore

# Creat function for /start commant 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Get the user's first name
  user_first_name = update.effective_user.first_name # type: ignore 
  # Takes user id from telegram
  user_id = update.effective_user.id
  mydb.user_value(user_id)
  await context.bot.send_message(
    # Send message to user
    chat_id = update.effective_chat.id, # type: ignore
    text = f"Hello {user_first_name}! \nI'm your personal note assistant. Here's what I can help you with:\n\n📝 *Create a New Note*\nSend me anything you'd like to save as a note, and I'll store it for you.\n\n🔍 *Search Your Notes*\nYou can browse by categories or search through your save notes.\n\n Choose an option:\n1️⃣ Type /create to starting creat new note.\n2️⃣ Use /categories to explore and search existing notes.\n\n💡 Tip: Organize your notes into categories to find them easily later!"
  )

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)


TITLE, CATEGORY, NOTE = range(3)

# Creat function for /create command 
async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):  
  # Ask user send title name
  await update.message.reply_text("✍️Send me the title for your note:")
  return TITLE

# Get title name from user
async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
  context.user_data['title'] = update.message.text
  await update.message.reply_text("🗂️Now send the category name:")
  return CATEGORY

# Get category name from user
async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
  context.user_data['category'] = update.message.text
  await update.message.reply_text("✍️Now send the note:")
  return NOTE


# Get note from user
async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
  context.user_data['note'] = update.message.text
  context.user_data['user_id'] = update.effective_user.id

  # Process the note
  user_id = context.user_data["user_id"]
  note = context.user_data['note']
  note_title = context.user_data['title']
  note_category = context.user_data['category']

  # Save data in database
  mydb.notes(note_title, note, note_category, user_id)
  
  # Conficmation message
  await update.message.reply_text(f"Your note was saved.\nTitle: {note_title}\nCategory: {note_category}\nNote: {note}\n\nYou can look to your notes sending /category")
  return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("create", create)],
    states={
        TITLE: [MessageHandler(filters.TEXT | filters.COMMAND, get_title)],
        CATEGORY: [MessageHandler(filters.TEXT | filters.COMMAND, get_category)],
        NOTE: [MessageHandler(filters.TEXT | filters.COMMAND, get_note)],
    },
    fallbacks=[],
)
application.add_handler(conv_handler)


# Creat function for /category command
async def category (update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id

  user_categories = mydb.categories(user_id)

  if not user_categories:
    await update.message.reply_text("☹️You don't have any saved categories yet.")
  # Extract and format
  categories = [row[0] for row in user_categories]
  formatted = "\n".join(f"📁 {cat}" for cat in categories)

  await update.message.reply_text(f"Your categories:\n {formatted}")


category_handler = CommandHandler('category', category)
application.add_handler(category_handler)

application.run_polling()