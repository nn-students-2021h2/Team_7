# -*- coding: utf-8 -*-
import json
# библиотека для загрузки данных из .env
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")  # bot token
# Optionally use an anonymizing proxy (SOCKS/HTTPS) if you encounter Telegram access issues in your region
PROXY = env.str("PROXY")

FACE_PP_API_KEY = env.str("FACE_PP_API_KEY")
FACE_PP_API_SECRET = env.str("FACE_PP_API_SECRET")
RAPID_API_KEY = env.str("RAPID_API_KEY")


# класс с данными из файла config.json
class ConfigSingleton:
    __instance = None

    def __init__(self):
        if not ConfigSingleton.__instance:
            # задает атрибуты из файла
            with open('config.json') as f:
                data = json.load(f)
            for key, value in data.items():
                if not hasattr(self, key):
                    print("add: ", key, value)
                    setattr(self, key, value)
        else:
            raise ValueError(f"Instance already created")

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = ConfigSingleton()
        return cls.__instance

    # обновление данных в файле
    def update(self):
        print(self.__dict__)
        with open('config.json', 'w') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)
