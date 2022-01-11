# pylint: skip-file
def send_message(msg, chat_id):
    pass


def photo_recognizing(photo):
    sex = None
    age = None
    return sex, age


def main(msg):
    photo = 'png'
    if msg.type == photo:
        sex, age = photo_recognizing(msg)
        text = f"Recognized:\n" \
               f"Sex: {sex}\n" \
               f"Age: {age}"
        send_message(text, msg.chat_id)
    else:
        text = 'I can recognize sex and age by the person`s photo. Send me png file'
        send_message(text, msg.chat_id)
