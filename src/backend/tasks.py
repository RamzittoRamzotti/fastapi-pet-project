import json
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from celery import Celery
from email.message import EmailMessage
import smtplib

from dotenv import load_dotenv

from src.backend.config import settings

cel = Celery('tasks', broker='redis://localhost:6379/0')
cel.config_from_object(settings.celery.config_celery)
cel.conf.broker_url = 'redis://localhost:6379/0'
cel.conf.broker_connection_retry_on_startup = True


def create_mail(recipient, body):
    msg = MIMEMultipart()
    msg['From'] = settings.celery.mail
    msg['To'] = recipient
    msg['Subject'] = "Бронирование книги"

    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ margin-bottom: 10px; }}
                img {{ max-width: 300px; height: auto; }}
            </style>
        </head>
        <body>
            <p>Вы успешно забронировали книгу:</p>
            <ul>
                <li><strong>Название:</strong> {body['title']}</li>
                <li><strong>Автор:</strong> {body['author']}</li>
                <li><img src="cid:image1" alt="{body['title']}"/></li>
            </ul>
        </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    img_path = os.path.join('./src/frontend/public/images',
                            body['title_picture'])
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()

    image = MIMEImage(img_data, name=os.path.basename(img_path), _subtype="png")
    image.add_header('Content-ID', '<image1>')
    image.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
    msg.attach(image)
    return msg


@cel.task
def send_mail(recipient, body):
    email = create_mail(recipient, body.dict())
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(settings.celery.mail, settings.celery.password)
        server.send_message(email)
