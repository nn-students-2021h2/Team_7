# -*- coding: utf-8 -*-
from io import BytesIO
import json

import requests
from PIL import Image, ImageDraw, ImageFont
from requests import RequestException
from telegram import File

from telegram_bot.config import (
    FACE_PP_API_KEY,
    FACE_PP_API_SECRET,
    RAPID_API_KEY,
    ConfigSingleton,
)

CONFIG = ConfigSingleton.get_instance()


def get_face_values(image_url: str) -> list:
    """Отправка запроса по API FACE++"""
    response = requests.post(
        CONFIG.face_pp_url,
        # 'https://api-us.faceplusplus.com/facepp/v3/detect',
        data={
            'api_key': FACE_PP_API_KEY,
            'api_secret': FACE_PP_API_SECRET,
            'image_url': image_url,
            'return_attributes': 'gender,age',
        },
    )
    if not response.ok:
        raise RequestException

    r_decode = json.loads(response.content.decode())
    return r_decode['faces']


def draw_rectangles(buf: BytesIO, faces: list) -> bytes:
    """Функция отрисовки подписей и прямоугольников по координатам лиц"""
    font = ImageFont.truetype('UbuntuMono.ttf', 36)
    with Image.open(buf) as photo:
        pencil = ImageDraw.Draw(photo)

        for face in faces:
            area = face['face_rectangle']
            pencil.rectangle(
                (
                    area['left'],  # x1
                    area['top'],  # y1
                    area['left'] + area['width'],  # x2
                    area['top'] + area['height'],  # y2
                )
            )
            # api отдает атрибуты только для первых 5 лиц
            if attr := face.get('attributes'):
                pencil.text(
                    xy=(area['left'], area['top']),
                    text=f"{attr['gender']['value']}, {attr['age']['value']}y.o.",
                    fill='green',
                    anchor='ld',
                    font=font,
                )

        with BytesIO() as new_img:
            # сохраняем новое изображение в буфер и сразу забираем в bytes
            photo.save(new_img, format='JPEG')
            byte_im = new_img.getvalue()

    return byte_im


def get_face_values_v2(image_url: str) -> list:
    """Отправка запроса по RAPID API"""
    response = requests.post(
        CONFIG.rapid_url,
        # 'https://face-detection6.p.rapidapi.com/img/face-age-gender',
        headers={
            'content-type': 'application/json',
            'x-rapidapi-host': 'face-detection6.p.rapidapi.com',
            'x-rapidapi-key': RAPID_API_KEY,
        },
        data=json.dumps({'url': image_url, 'accuracy_boost': 3}),
    )
    if not response.ok:
        raise RequestException

    r_decode = json.loads(response.content.decode())
    return r_decode['detected_faces']


def draw_rectangles_v2(buf: BytesIO, faces: list) -> bytes:
    """Функция отрисовки подписей и прямоугольников по координатам лиц"""
    font = ImageFont.truetype('UbuntuMono.ttf', 32)
    with Image.open(buf) as photo:
        pencil = ImageDraw.Draw(photo)

        for face in faces:
            area = face['BoundingBox']
            pencil.rectangle((area['startX'], area['startY'], area['endX'], area['endY']))
            pencil.text(
                xy=(area['startX'], area['startY']),
                text=f"{face['Gender']['Gender']}, "
                     f"{face['Age']['Age-Range']['Low']}-{face['Age']['Age-Range']['High']}y.o.",
                fill='green',
                anchor='la',
                font=font,
            )

        with BytesIO() as new_img:
            # сохраняем новое изображение в буфер и сразу забираем в bytes
            photo.save(new_img, format='JPEG')
            byte_im = new_img.getvalue()

    return byte_im


def processing_image(photo: File) -> [bytes]:
    face_values = get_face_values_v2(photo.file_path)
    if not face_values:
        return None

    with BytesIO() as buf:
        photo.download(out=buf)  # загружаем фото из сообщения в буфер
        photo_bytes = draw_rectangles_v2(buf, face_values)

    return photo_bytes
