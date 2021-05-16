from settings import mail
from flask_mail import Message
from flask import render_template


def send_standard_message(title, body, recipients):
    msg_html = render_template(
        "messages/messageBase.html",
        body=body,
        email='',
        phone=''
    )
    
    msg = Message(
        title, sender='test@mail.ru', recipients=recipients, html=msg_html)
    
    mail.send(msg)
