import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Logging sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot tokeni va admin ID sini shu yerga kiriting:
API_TOKEN = "8217204836:AAF0WyNn1_Aop2qXoiylCl-7yQQy6w5hKK4"
ADMIN_ID = 6578880988

# Kinolar ma'lumotlar bazasi (kod => url)
movies_db = {}

# Admin uchun kino qo'shish komandasi: /addmovie kod url
def add_movie(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        if len(context.args) < 2:
            update.message.reply_text("Iltimos, kino kodini va URL manzilini kiriting.\nMasalan: /addmovie 12345 https://kino-link.com")
            return
        movie_code = context.args[0]
        movie_url = context.args[1]
        movies_db[movie_code] = movie_url
        update.message.reply_text(f"Kino '{movie_code}' kodi bilan qo'shildi.")
    else:
        update.message.reply_text("Siz admin emassiz!")

# Foydalanuvchidan kino kodini qabul qilish va kino URLni yuborish
def get_movie(update: Update, context: CallbackContext):
    movie_code = update.message.text.strip()
    if movie_code in movies_db:
        update.message.reply_text(f"Kino topildi:\n{movies_db[movie_code]}")
    else:
        update.message.reply_text("Kechirasiz, bunday kino kodi topilmadi.")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom! Iltimos, kino kodi yuboring.")

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addmovie", add_movie))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_movie))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
