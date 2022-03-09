import json

from telegram_bot.config import json_path, logger


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
