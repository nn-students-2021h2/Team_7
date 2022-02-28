# -*- coding: utf-8 -*-
import logging
from pathlib import Path

# библиотека для загрузки данных из .env
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


json_path = Path(Path(__file__).parent, 'config.json')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
