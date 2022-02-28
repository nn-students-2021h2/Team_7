# -*- coding: utf-8 -*-
# pylint: C0412
import logging

from telegram import Bot, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from db.db_worker import add_person, increase_requests_count, get_user_requests_count, get_users_count, get_user
from db.models import User, Base
from telegram_bot.config import TOKEN, engine
from misc.singleton import ConfigSingleton
from telegram_bot.ping_site import ping
from telegram_bot.recognize import processing_image

# pylint: disable=W0613, R0801

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
CONFIG = ConfigSingleton.get_instance()


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет \U0001F44B, {update.effective_user.first_name}!')
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    full_name = update.effective_user.full_name
    add_person(User(user_id=user_id, user_name=user_name, full_name=full_name))
    update.message.reply_text('Отправь мне фото\U0001F4F7.\n'
                              'Я распознаю на нём лица и определю пол и возраст\U0001F440')


def get_ping(update: Update, context: CallbackContext):
    """Get ping"""
    min_time, max_time, avg_time = ping()
    update.message.reply_text(f'\U0001F310 Пинг:\n{min_time=}\n{max_time=}\n{avg_time=}')


def user_requests_count(update: Update, context: CallbackContext):
    """get user requests count"""
    count = get_user_requests_count(update.effective_user.id)
    if count is None:
        update.message.reply_text('Тебя нет в базе\U0001F97A\n'
                                  'Нажми /start, чтобы это исправить!')
    elif count == 0:
        update.message.reply_text('\U0001F9EE Ты еще не делал запросов!')
    else:
        update.message.reply_text(f'\U0001F9EE Число запросов: {count}!')


def users_count(update: Update, context: CallbackContext):
    """get users count"""
    count = get_users_count()
    update.message.reply_text(f'\U0001F465 Число юзеров: {count}!')


def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    text = "Я умею распознавать людей на фотографии\U0001F440.\n" \
           "Отправь мне фото.\n" \
           "\U0001F916 /start - запуск бота\n" \
           "\U00002753 /help - справка\n" \
           "\U0001F9EE /my_count - количество твоих распознаваний\n" \
           "\U0001F465 /users_count - количество пользователей бота"
    update.message.reply_text(text)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')
    update.message.reply_text('Упс... Что-то пошло не так. Попробуй позже')


def photo_recognize(update: Update, context: CallbackContext):
    """Поиск лиц на фото, отправка обработанного изображения"""

    # проверка есть ли пользователь в базе
    user = get_user(update.effective_user.id)
    if not user:
        update.message.reply_text('Тебя нет в базе\U0001F97A\n'
                                  'Нажми /start, чтобы это исправить и пользоваться ботом!')
        return

    # проверка превышения лимита
    if CONFIG.total_max_requests > CONFIG.current_requests:
        input_photo = bot.get_file(update.message.photo[-1]['file_id'])
        update.message.reply_text('\U0001F440 Обработка изображения...')
        CONFIG.current_requests += 1
        logger.info(f'Current requests: {CONFIG.current_requests}')
        # print(f'[INFO] Current requests: {CONFIG.current_requests}')
        CONFIG.update()

        increase_requests_count(update.effective_user.id)

        output_photo = processing_image(input_photo)

        if output_photo:
            update.message.reply_photo(photo=output_photo)
        else:
            update.message.reply_text('Лица не найдены \U0001F613\n'
                                      'Попробуй другое фото')
    else:
        update.message.reply_text('Месячный лимит исчерпан \U0001F615')


def unidentified(update: Update, context: CallbackContext):
    """Обработка ситуации с неизвестным вложением в сообщении"""
    update.message.reply_text('Я умею работать только с прикрепленными изображениями')


if __name__ == '__main__':
    # create tables
    logger.info('Create tables')
    Base.metadata.create_all(engine)

    logger.info('Start Bot')

    updater = Updater(bot=bot, use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))
    updater.dispatcher.add_handler(CommandHandler('my_count', user_requests_count))
    updater.dispatcher.add_handler(CommandHandler('users_count', users_count))
    updater.dispatcher.add_handler(CommandHandler('ping', get_ping))

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
