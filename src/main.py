import os

from src.constants.constants import WELCOME_TEXT

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def get_main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Пароли"),
             KeyboardButton("CRM")],
            [KeyboardButton("Контакты")]
        ],
        resize_keyboard=True
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(WELCOME_TEXT)
    await update.message.reply_text(
        "Выберите действие, используя кнопки меню:",
        reply_markup=get_main_menu()
    )


async def menu_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == "🏠 Главное меню":
        await update.message.reply_text("Вы вернулись в главное меню!", reply_markup=get_main_menu())
    elif text == "ℹ️ О нас":
        await update.message.reply_text("Этот бот помогает новым сотрудникам адаптироваться в Artego Estate! 🏡")
    elif text == "📞 Контакты":
        await update.message.reply_text("Свяжитесь с нами по email: contact@artegoestate.com")
    else:
        await update.message.reply_text("Я вас не понял. Используйте кнопки меню.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
