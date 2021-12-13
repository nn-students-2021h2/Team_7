import requests
import json

from telegram_bot.recgtn import recognition

TOKEN = ''
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
DOWNLOAD_URL = f'https://api.telegram.org/file/bot{TOKEN}/'
LONG_POLLING_TIMEOUT = 10


def get_photo(msg):
    photos = msg.get('photo')
    if photos:
        file_id = photos[-1]['file_id']
        r = requests.get(BASE_URL + f'getFile?file_id={file_id}')
        file_path = r.json()['result']['file_path']
        photo_bytes = requests.get(DOWNLOAD_URL + file_path).content
        return photo_bytes
    return


def send_photo(chat_id, photo_bytes, caption=''):
    files = {
        'photo': photo_bytes
    }
    if caption:
        message = (BASE_URL + f'sendPhoto?chat_id={chat_id}&caption={caption}')
    else:
        message = (BASE_URL + f'sendPhoto?chat_id={chat_id}')
    send = requests.post(message, files=files)


def send_message(chat_id, message):
    requests.post(BASE_URL + 'sendMessage', params={
        "chat_id": chat_id,
        "text": message
    })


def start_poling():
    last_update_id = None
    while True:
        r = requests.get(BASE_URL + 'getUpdates',
                         params={
                             'offset': last_update_id,
                             'timeout': LONG_POLLING_TIMEOUT
                         })
        response_dict = json.loads(r.text)
        for upd in response_dict["result"]:
            last_update_id = upd["update_id"] + 1
            # print(upd)
            msg = upd["message"]
            # print(msg)
            chat_id = msg["chat"]["id"]

            photo_bytes = get_photo(msg)
            if photo_bytes:
                text = 'Ты отправил фото. Жди результат'
                send_message(chat_id, text)
                rec = recognition(photo_bytes)
                if rec:
                    gender, age, photo_bytes = rec
                    caption = 'Recognized:\n' \
                              f'Gender: {gender}\n' \
                              f'Age: {age}'
                    send_photo(chat_id, photo_bytes, caption)
                else:
                    text = 'Ups...\n' \
                           'I can`t'
                    send_message(chat_id, text)
            else:
                text = 'Ты не отправил фото'
                send_message(chat_id, text)


start_poling()
