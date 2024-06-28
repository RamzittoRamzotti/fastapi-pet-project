import json
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
    msg = EmailMessage()
    msg['From'] = settings.celery.mail
    msg['To'] = recipient
    msg['Subject'] = "Бронирование книги"

    html_content = f"""
                <p>Вы забронировали книгу:</p>
                <ul>
                    <li>{body['title']}</li>
                    <li>{body['author']}</li>
                    <li><img src="http://localhost:5000/images/{body['title_picture']}" alt="{body['title']}"/></li>
                </ul>'
        """
    msg.set_content(html_content, subtype='html')
    return msg


@cel.task
def send_mail(recipient, body):
    email = create_mail(recipient, body.dict())
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(settings.celery.mail, settings.celery.password)
        server.send_message(email, settings.celery.mail, recipient)
