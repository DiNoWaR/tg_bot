import os

from src.constants.constants import *

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from telegram.constants import ParseMode

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ONBOARDING_DOC_LINK = os.getenv('ONBOARDING_DOC_LINK')

onboarding_file_id = ''


def get_main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(PASSWORDS),
             KeyboardButton(АMO_CRM)],
            [KeyboardButton(CONTACTS),
             KeyboardButton(ONBOARDING)]
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
    elif text == ONBOARDING:
        await update.message.reply_document(document=onboarding_file_id, caption="Onboarding Document 📄")
    else:
        await update.message.reply_text('Я вас не понял. Используйте кнопки меню.')


async def get_file_id(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    if document:
        file_id = document.file_id
        onboarding_file_id = file_id


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, get_file_id))

    app.run_polling()


if __name__ == '__main__':
    main()
