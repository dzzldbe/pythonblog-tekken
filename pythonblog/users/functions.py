import os
import secrets

from flask import current_app, url_for
from flask_mail import Message
from PIL import Image

from pythonblog import mail
from pythonblog.models import User


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    file_name = random_hex + file_ext
    file_path = os.path.join(current_app.root_path, f"static/profile_pics/{file_name}")
    output_size = (125, 125)
    with Image.open(form_picture) as img:
        img.thumbnail(output_size)
        # ImageOps.contain(img, output_size)
        img.save(file_path)

    return file_name


def send_email(user):
    token = User.get_reset_token(user)
    msg = Message(
        subject="Password Reset Request",
        recipients=[user.email],
        sender=os.environ.get("MY_GMAIL"),
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for("users.reset_password", token=token, _external=True)}
If you did not make this request, please ignore it"""

    mail.send(msg)
