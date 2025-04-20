import os

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

from src.constants.constants import *
from src.parser.config_parser import ConfigParser

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

parser = ConfigParser()

bot_config = parser.parse_config()


def get_main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(LEARNING), KeyboardButton(ONBOARDING), KeyboardButton(ANALYTICS), KeyboardButton(AMO_CRM), KeyboardButton(PARTNER_PROGRAM)],
            [KeyboardButton(PASSWORDS), KeyboardButton(SECONDARY), KeyboardButton(GROUPS), KeyboardButton(CONTACTS)]
        ],
        resize_keyboard=True
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(bot_config.welcome_message)
    await update.message.reply_document(bot_config.handbook_file_id)
    await update.message.reply_text(bot_config.welcome_message_buttons, reply_markup=get_main_menu())


async def menu_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower().replace(' ', '_')

    for item in bot_config.menu:
        if item.title == text:
            for response in item.responses:
                if response.type == 'text':
                    await update.message.reply_text(response.content)
                if response.type == 'document':
                    await update.message.reply_document(document=response.file_id)
            return

    await update.message.reply_text(bot_config.default_reply)


async def get_file_id(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    if document:
        file_id = document.file_id
        await update.message.reply_text(f"Ваш file_id: {file_id}")


def main():
    app = Application.builder().token(bot_token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, get_file_id))

    app.run_polling()


if __name__ == '__main__':
    main()
