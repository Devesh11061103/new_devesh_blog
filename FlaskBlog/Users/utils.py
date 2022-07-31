import os
import secrets
import smtplib

from PIL import Image
from flask import url_for, current_app
from flask_login import current_user


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ex = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ex
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    prev = os.path.join(current_app.root_path, "static/profile_pics", current_user.image_file)
    if os.path.exists(prev):
        if current_user.image_file != "default.jpg":
            os.remove(prev)
    return picture_fn


def send_email(user):
    my_email = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    print(my_email)
    print(password)
    token = user.get_reset_token()
    # print(token)
    msg = f"To Reset your Password, visit the following link: \n{url_for('users.reset_token', token=token, _external=True)} \n\nIf you did not make this request simply ignore this email and no changes will be made to your account "
    with smtplib.SMTP("smtp.gmail.com", port=587) as new_connection:
        new_connection.starttls()
        new_connection.login(user=my_email, password=password)
        new_connection.sendmail(from_addr=my_email, to_addrs=user.email,
                                msg=f"Subject: Reset Password\n\n{msg}")
