# -*- coding: utf-8 -*-
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Tuple

import requests

from telegram_bot.config import ConfigSingleton

CONFIG = ConfigSingleton.get_instance()
logger = logging.getLogger(__name__)

min_time = max_time = avg_time = last_request = None

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
    global avg_time, min_time, max_time, last_request

    # Выполнение запросов не чаще одного раза в минуту
    if not last_request or (datetime.now() - last_request).seconds > 60:

        with ThreadPoolExecutor(32) as pool:
            for _ in range(10):
                future = pool.submit(ping_site)
                future.result()

        min_time = min(response_times) / 1_000_000
        max_time = max(response_times) / 1_000_000
        avg_time = (sum(response_times) / 1_000_000) / len(response_times)

        last_request = datetime.now()
        response_times.clear()

    logger.info(f'PING SITE: {min_time=}, {max_time=}, {avg_time=}')
    return min_time, max_time, avg_time
