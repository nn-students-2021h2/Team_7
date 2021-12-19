# -*- coding: utf-8 -*-
from io import BytesIO
import json

import requests
from PIL import Image, ImageDraw, ImageFont
from telegram import File

from telegram_bot.setup import API_KEY, API_SECRET


def get_face_values(image_url: str) -> list:
    """Отправка запроса по API FACE++"""
    result = requests.post(
        'https://api-us.faceplusplus.com/facepp/v3/detect',
        data={
            'api_key': API_KEY,
            'api_secret': API_SECRET,
            'image_url': image_url,
            'return_attributes': 'gender,age'
        }
    )

    r_decode = json.loads(result.content.decode())
    return r_decode['faces']


def draw_rectangles(buf: BytesIO, faces: list) -> bytes:
    """Функция отрисовки подписей и прямоугольников по координатам лиц"""
    font = ImageFont.truetype('UbuntuMono.ttf', 36)
    with Image.open(buf) as photo:
        pencil = ImageDraw.Draw(photo)

        for face in faces:
            area = face['face_rectangle']
            # окантовка
            pencil.rectangle((
                area['left'],                   # x1
                area['top'],                    # y1
                area['left'] + area['width'],   # x2
                area['top'] + area['height']    # y2
            ))
            # api отдает атрибуты только для первых 5 лиц
            if attr := face.get('attributes'):
                # подпись
                pencil.text(
                    xy=(area['left'], area['top']),
                    text=f"{attr['gender']['value']}, {attr['age']['value']}y.o.",
                    fill='green', anchor='ld', font=font
                )

        with BytesIO() as new_img:
            photo.save(new_img, format='JPEG')  # сохраняем новое изображение в буфер и сразу забираем в bytes
            byte_im = new_img.getvalue()

    return byte_im


def processing_image(photo: File) -> [bytes]:
    """Общая функция работы с изображением"""
    face_values = get_face_values(photo.file_path)
    if not face_values:
        return

    with BytesIO() as buf:
        photo.download(out=buf)  # загружаем фото из сообщения в буфер
        photo_bytes = draw_rectangles(buf, face_values)

    return photo_bytes

