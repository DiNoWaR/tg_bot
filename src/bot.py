import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Дальше ➡️", callback_data="next")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Нажми кнопку, чтобы продолжить: ', reply_markup=reply_markup)


async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.edit_text("Вы нажали 'Дальше'. Вот новое сообщение!")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
