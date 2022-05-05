from flask_mail import Mail, Message

from src.app import app

mail = Mail(app)


def send_message(**kwargs):
    msg = Message(**kwargs)

    with app.app_context():
        mail.send(msg)
