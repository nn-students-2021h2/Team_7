from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.models import User
from misc.async_wraps import run_blocking_io

from telegram_bot.config import engine
# pylint: disable=C0103


def add_person(user: User):
    """
    Добавление юзера в бд

    :param user:
    :return:
    """
    with Session(engine) as s:
        # session = sessionmaker(bind=engine)
        # s = session()
        try:
            s.add(user)
            s.commit()
        except IntegrityError:
            pass


async def async_add_person(user: User):
    await run_blocking_io(add_person, user)


def increase_requests_count(user_id):
    """
    Увеличение счетчика запросов пользователя

    :param user_id:
    :return:
    """
    with Session(engine) as s:
        # session = sessionmaker(bind=engine)
        # s = session()
        s.query(User).filter(User.user_id == user_id).update({User.requests_count: User.requests_count + 1})
        s.commit()


async def async_increase_requests_count(user_id):
    await run_blocking_io(increase_requests_count, user_id)


def get_users_count() -> int:
    """
    Количество пользователей бота

    :return:
    """
    with Session(engine) as s:
        # session = sessionmaker(bind=engine)
        # s = session()
        return s.query(User.user_id).count()


async def async_get_users_count():
    return await run_blocking_io(get_users_count)


def get_user_requests_count(user_id) -> int:
    """
    Количество запросов пользователя

    :param user_id:
    :return:
    """
    with Session(engine) as s:
        # session = sessionmaker(bind=engine)
        # s = session()
        return s.query(User.requests_count).filter(User.user_id == user_id).scalar()


async def async_get_user_requests_count(user_id):
    return await run_blocking_io(get_user_requests_count, user_id)


def get_user(user_id) -> User:
    """
    Получить пользователя по id

    :param user_id:
    :return:
    """
    with Session(engine) as s:
        # session = sessionmaker(bind=engine)
        # s = session()
        return s.query(User).filter(User.user_id == user_id).scalar()


async def async_get_user(user_id):
    return await run_blocking_io(get_user, user_id)
