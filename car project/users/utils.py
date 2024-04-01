import os
import secrets
from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from carproject import mail

def save_picture(form_picture, way: str, size_ox: int, size_oy: int):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, f'static/{way}', picture_fn)

    output_size = (size_ox, size_oy)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Запит На Зміну Паролю',
                  sender='noreplier228@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Щоб змінити пароль, буль ласка перейдіть за цим посиланням:
{url_for('users.reset_token', token=token, _external=True)}

Якщо ви не робили цей запит, то просто проігноруйте цей лист і ніяких змін не відбудеться.
'''
    mail.send(msg)

def send_confirmation_email(user):
    token = user.get_reset_token()
    msg = Message('Підтвердження Реєстрації',
                  sender='noreplier228@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Щоб підтвердити вашу реєстрацію, будь ласка перейдіть за цим посиланням:
{url_for('users.confirm_email', token=token, _external=True)}

Якщо ви не робили цей запит, то просто проігноруйте цей лист і ніяких змін не відбудеться.
'''
    mail.send(msg)