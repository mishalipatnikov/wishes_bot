from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import logging

from services.wishes_generator import WishesGenerator


class TelegramIntegrations:
    def __init__(self, token: str, wishes_generator: WishesGenerator):
        self._logger = logging.getLogger()
        self._application = None
        self._token = token
        self._wishes_generator = wishes_generator

    def initialize(self):
        self._application = ApplicationBuilder().token(self._token).build()

        start_handler = CommandHandler('wishes', self._start)
        self._application.add_handler(start_handler)

        help_handler = CommandHandler('help', self._help_command)
        self._application.add_handler(help_handler)

        self._application.add_handler(CallbackQueryHandler(self._button_handler))

        unknown_handler = MessageHandler(filters.COMMAND, self._unknown)
        self._application.add_handler(unknown_handler)

        return self

    def run(self):
        self._application.run_polling()
        return self

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._logger.info(f'Receive get wishes command from: {update.message.chat.full_name}. Create option buttons.')
        keyboard = [
            [InlineKeyboardButton("Простое🤭", callback_data='simple_wish')],
            [InlineKeyboardButton("Сложное🥳", callback_data='complex_wish')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Пожалуйста, выберите поздравление🥳:', reply_markup=reply_markup)

    async def _button_handler(self, update, _):
        query = update.callback_query
        variant = query.data

        self._logger.info(f'Receive buttons result from: {query.message.chat.full_name}. Result is {variant}')

        await query.answer()

        if variant == 'simple_wish':
            wish = self._wishes_generator.get_simple_wish()
        elif variant == 'complex_wish':
            wish = self._wishes_generator.get_complex_wish()
        else:
            raise Exception(f'Unknown button variant: `{variant}`')

        await query.edit_message_text(text=wish)

    async def _help_command(self, update, _):
        self._logger.info(f'Receive help command from: {update.message.chat.full_name}.')
        await update.message.reply_text("Используйте `/wishes` для поздравления.")

    async def _unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._logger.info(f'Receive unknown command from: {update.message.chat.full_name}.')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю ©Песков 🤡")
