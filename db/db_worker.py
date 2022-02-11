from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.models import User

from telegram_bot.config import engine


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


def get_users_count() -> int:
    """
    Количество пользователей бота

    :return:
    """
    with Session(engine) as s:
        # session = sessionmaker(bind=engine)
        # s = session()
        return s.query(User.user_id).count()


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


def get_user(user_id) -> User:
    with Session(engine) as s:
        # session = sessionmaker(bind=engine)
        # s = session()
        return s.query(User).filter(User.user_id == user_id).scalar()
