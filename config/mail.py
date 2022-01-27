from config.settings import app
from flask_mail import Message
from flask_mail import Mail

mail = Mail(app)


def send_message(subject, body, recipients=['teisanutudort@gmail.com']):
    msg = Message(
        subject=subject, sender='Johny', recipients=recipients, body=body)

    mail.send(msg)


def send_email_link(email, link):
    body = f'{link}'
    send_message('Reset password', body=body, recipients=[email])
