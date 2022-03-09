import json

from jsonschema import validate

from telegram_bot.config import json_path, logger


class ConfigSingleton:
    """Класс-синглтон с данными из файла config.json"""
    __instance = None

    def __init__(self):

        if ConfigSingleton.__instance:
            raise ValueError('Instance already created')

        with open(json_path, encoding='UTF-8') as config:
            data = json.load(config)
            self.check_config(data)
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
        with open(json_path, 'w', encoding='UTF-8') as config:
            json.dump(self.__dict__, config, ensure_ascii=False, indent=4)

    @staticmethod
    def check_config(data: dict):
        """Метод валидации конфиг-файла"""
        validation_schema = {
            "type": "object",
            "properties": {
                "total_max_requests": {"type": "number"},
                "current_requests": {"type": "number"},
                "rapid_url": {"type": "string"},
                "rapid_site": {"type": "string"}
            },
            "additionalProperties": True
        }
        validate(instance=data, schema=validation_schema)

    # TODO
    # add scheduler for update current_requests in config.json every month
