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
    
def send_test_message():
    # msg_html = render_template(
    #     "messages/messageBase.html",
    #     body=body,
    #     email='',
    #     phone=''
    # )

    msg = Message(
        subject='no-reply', sender='Johny', recipients=['teisanutudort@gmail.com'], body='test body')
    
    mail.send(msg)
