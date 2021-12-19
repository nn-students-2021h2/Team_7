# -*- coding: utf-8 -*-
import logging

from setup import TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from telegram_bot.recognize import processing_image

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')
    update.message.reply_text('Отправь мне фото. Я распознаю на нём лица и определю пол и возраст')


def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала')


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')
    update.message.reply_text('Упс... Что-то пошло не так. Попробуй позже')


def photo_recognize(update: Update, context: CallbackContext):
    """Поиск лиц на фото, отправка обработанного изображения"""
    update.message.reply_text('Обработка изображения...')
    input_photo = bot.get_file(update.message.photo[-1]['file_id'])
    output_photo = processing_image(input_photo)

    if output_photo:
        update.message.reply_photo(photo=output_photo)
    else:
        update.message.reply_text('Лица не найдены. Попробуй другое фото')


def unidentified(update: Update, context: CallbackContext):
    update.message.reply_text('Я умею работать только с прикрепленными изображениями')


def main():
    updater = Updater(bot=bot, use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))

    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_recognize))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, unidentified))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
