# -*- coding: utf-8 -*-
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Tuple

import requests

from telegram_bot.config import ConfigSingleton

CONFIG = ConfigSingleton.get_instance()
logger = logging.getLogger(__name__)

MIN_TIME = MAX_TIME = AVG_TIME = LAST_REQUEST = None

response_times = []


def ping_site() -> None:
    """Функция получения времени ответа на GET-запрос"""
    global response_times
    response = requests.get(CONFIG.rapid_site)
    if response.ok:
        response_times.append(response.elapsed.microseconds)  # значения маленькие, поэтому храним в мкс


def ping() -> Tuple[int, int, int]:
    """Функция для пинга сайта и получения связки максимального, минимального и среднего времени ответа"""
    # Полученные значения и время последнего запроса лежат глобально
    global AVG_TIME, MIN_TIME, MAX_TIME, LAST_REQUEST

    # Выполнение запросов не чаще одного раза в минуту
    if not LAST_REQUEST or (datetime.now() - LAST_REQUEST).seconds > 60:

        with ThreadPoolExecutor(8) as pool:
            for _ in range(10):
                future = pool.submit(ping_site)
                future.result()

        MIN_TIME = min(response_times) / 1_000_000
        MAX_TIME = max(response_times) / 1_000_000
        AVG_TIME = (sum(response_times) / 1_000_000) / len(response_times)

        LAST_REQUEST = datetime.now()
        response_times.clear()

    logger.info(f'PING SITE: {MIN_TIME=}, {MAX_TIME=}, {AVG_TIME=}')
    return MIN_TIME, MAX_TIME, AVG_TIME
