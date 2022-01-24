# -*- coding: utf-8 -*-
import logging

from telegram import Bot, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from telegram_bot.config import TOKEN, ConfigSingleton
from telegram_bot.recognize import processing_image

# pylint: disable=W0613

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
CONFIG = ConfigSingleton.get_instance()


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
    # проверка превышения лимита
    if CONFIG.total_max_requests > CONFIG.current_requests:
        input_photo = bot.get_file(update.message.photo[-1]['file_id'])
        update.message.reply_text('Обработка изображения...')
        CONFIG.current_requests += 1
        logger.info(f'Current requests: {CONFIG.current_requests}')
        # print(f'[INFO] Current requests: {CONFIG.current_requests}')
        CONFIG.update()
        output_photo = processing_image(input_photo)

        if output_photo:
            update.message.reply_photo(photo=output_photo)
        else:
            update.message.reply_text('Лица не найдены. Попробуй другое фото')
    else:
        update.message.reply_text('Месячный лимит исчерпан')


def unidentified(update: Update, context: CallbackContext):
    """Обработка ситуации с неизвестным вложением в сообщении"""
    update.message.reply_text('Я умею работать только с прикрепленными изображениями')


if __name__ == '__main__':
    logger.info('Start Bot')

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
