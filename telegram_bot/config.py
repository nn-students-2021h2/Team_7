# -*- coding: utf-8 -*-
import json

# библиотека для загрузки данных из .env
import logging
import os

from environs import Env
from sqlalchemy import create_engine

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")  # bot token
# Optionally use an anonymizing proxy (SOCKS/HTTPS) if you encounter Telegram access issues in your region
PROXY = env.str("PROXY")

FACE_PP_API_KEY = env.str("FACE_PP_API_KEY")
FACE_PP_API_SECRET = env.str("FACE_PP_API_SECRET")
RAPID_API_KEY = env.str("RAPID_API_KEY")
DATABASE = env.str("DATABASE")

# подключение к бд
engine = create_engine(f"sqlite:///{DATABASE}"
                       "?check_same_thread=False")

json_path = os.path.join(os.path.dirname(__file__), 'config.json')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigSingleton:
    """Класс-синглтон с данными из файла config.json"""

    __instance = None

    def __init__(self):

        if ConfigSingleton.__instance:
            raise ValueError('Instance already created')

        with open(json_path, encoding='UTF-8') as config:
            data = json.load(config)
        for key, value in data.items():
            if not hasattr(self, key):
                logger.info(f'add: {key} {value}')
                setattr(self, key, value)

    @classmethod
    def get_instance(cls):
        """Метод создания/получения единственного объекта класса"""
        if not cls.__instance:
            cls.__instance = ConfigSingleton()
        return cls.__instance

    def update(self):
        """Обновление данных в файле"""
        logger.info(self.__dict__)
        with open('config.json', 'w', encoding='UTF-8') as config:
            json.dump(self.__dict__, config, ensure_ascii=False, indent=4)

    # TODO
    # add scheduler for update current_requests in config.json every month
