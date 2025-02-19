import os

from src.constants.constants import *

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def get_main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(PASSWORDS),
             KeyboardButton(АMO_CRM)],
            [KeyboardButton(CONTACTS)]
        ],
        resize_keyboard=True
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(WELCOME_TEXT)
    await update.message.reply_text(
        'Выберите действие, используя кнопки меню',
        reply_markup=get_main_menu()
    )


async def menu_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == АMO_CRM:
        await update.message.reply_text('Вы вернулись в главное меню!', reply_markup=get_main_menu())
    elif text == PASSWORDS:
        await update.message.reply_text(PASSWORDS_TEXT)
    elif text == CONTACTS:
        await update.message.reply_text('contacts!')
    else:
        await update.message.reply_text('Я вас не понял. Используйте кнопки меню.')


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    app.run_polling()


if __name__ == '__main__':
    main()
