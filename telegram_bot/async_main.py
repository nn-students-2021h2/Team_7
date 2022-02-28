import logging
# pylint: disable=R0801, duplicate-code

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import File

from db.db_worker import async_add_person, async_get_user_requests_count, async_get_users_count, \
    async_increase_requests_count, async_get_user
from db.models import User

from telegram_bot.config import TOKEN
from telegram_bot.ping_site import async_ping
from telegram_bot.recognize import async_processing_image

from misc.singleton import ConfigSingleton

# pylint: disable=W0613, C0412

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
CONFIG = ConfigSingleton.get_instance()


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    """Get ping"""
    await message.answer(f'Привет \U0001F44B, {message.from_user.first_name}!')
    user_id = message.from_user.id
    user_name = message.from_user.username
    full_name = message.from_user.full_name
    # надо сделать асинхронное обращение к бд для хорошей работы
    await async_add_person(User(user_id=user_id, user_name=user_name, full_name=full_name))
    await message.answer('Отправь мне фото\U0001F4F7\n'
                         'Я распознаю на нём лица и определю пол и возраст\U0001F440')


@dp.message_handler(Command('help'))
async def chat_help(message: types.Message):
    """Send a message when the command /help is issued."""
    text = "Я умею распознавать людей на фотографии\U0001F440.\n" \
           "Отправь мне фото.\n" \
           "\U0001F916 /start - запуск бота\n" \
           "\U00002753 /help - справка\n" \
           "\U0001F9EE /my_count - количество твоих распознаваний\n" \
           "\U0001F465 /users_count - количество пользователей бота"
    await message.answer(text)


@dp.message_handler(Command('ping'))
async def get_ping(message: types.Message):
    """get user requests count"""
    min_time, max_time, avg_time = await async_ping()
    await message.answer('\U0001F310 Пинг:\n'
                         f'Минимальное время: {min_time}\n'
                         f'Максимальное время: {max_time}\n'
                         f'Среднее время: {avg_time}')


@dp.message_handler(Command('my_count'))
async def user_requests_count(message: types.Message):
    """get users count"""
    count = await async_get_user_requests_count(message.from_user.id)
    if count is None:
        await message.answer('Тебя нет в базе\U0001F97A\n'
                             'Нажми /start, чтобы это исправить!')
    elif count == 0:
        await message.answer('\U0001F9EE Ты еще не делал запросов!')
    else:
        await message.answer(f'\U0001F9EE Число запросов: {count}!')


@dp.message_handler(Command('users_count'))
async def users_count(message: types.Message):
    """Send a message when the command /help is issued."""
    count = await async_get_users_count()
    await message.answer(f'\U0001F465 Число юзеров: {count}!')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_recognize(message: types.Message):
    """Поиск лиц на фото, отправка обработанного изображения"""

    # проверка есть ли пользователь в базе
    user = await async_get_user(message.from_user.id)
    if not user:
        await message.answer('Тебя нет в базе\U0001F97A\n'
                             'Нажми /start, чтобы это исправить и пользоваться ботом!')
        return

    # проверка превышения лимита
    if CONFIG.total_max_requests > CONFIG.current_requests:
        input_photo: File = await bot.get_file(message.photo[-1].file_id)
        await message.answer('\U0001F440 Обработка изображения...')
        CONFIG.current_requests += 1
        logger.info(f'Current requests: {CONFIG.current_requests}')
        # print(f'[INFO] Current requests: {CONFIG.current_requests}')
        CONFIG.update()

        await async_increase_requests_count(message.from_user.id)

        output_photo = await async_processing_image(input_photo)

        if output_photo:
            await message.answer_photo(photo=output_photo)
        else:
            await message.answer('Лица не найдены \U0001F613\n'
                                 'Попробуй другое фото')
    else:
        await message.answer('Месячный лимит исчерпан \U0001F615')


@dp.message_handler()
async def echo(message: types.Message):
    """Обработка ситуации с неизвестным вложением в сообщении"""
    await message.answer('Я умею работать только с прикрепленными изображениями')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
