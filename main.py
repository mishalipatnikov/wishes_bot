import telegram
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, Updater, \
    CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

TOKEN = "{TOKEN}"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="I'm a bot, please talk to me!"
    # )
    # keyboard = [
    #     [
    #         InlineKeyboardButton("Option 1", callback_data='1'),
    #         InlineKeyboardButton("Option 2", callback_data='2'),
    #     ],
    #     [InlineKeyboardButton("Option 3", callback_data='3')],
    # ]

    keyboard = [
        [InlineKeyboardButton("Простое🤭", callback_data='1')],
        [InlineKeyboardButton("Сложное🥳", callback_data='2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Пожалуйста, выберите поздравление🥳:', reply_markup=reply_markup)


async def button(update, _):
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    # смотри https://core.telegram.org/bots/api#callbackquery.
    await query.answer()
    # редактируем сообщение, тем самым кнопки
    # в чате заменятся на этот ответ.
    await query.edit_message_text(text=f"Выбранный вариант: {variant}")


async def help_command(update, _):
    await update.message.reply_text("Используйте `/wishes` для поздравления.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю ©Песков 🤡")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('wishes', start)
    application.add_handler(start_handler)
    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)
    application.add_handler(CallbackQueryHandler(button))
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)


    # start
    application.run_polling()
