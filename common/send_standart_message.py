from settings import mail, app
from flask_mail import Message
from config import backendAddress
from flask import render_template
# from models.common_settings import CommonSettings
# from config import mailSender

mail_sender = 'flask@mail.com'


def sendStandartMessage(title, body, recipients):
    msg_html = render_template(
        "messages/messageBase.html",
        logoUrl=backendAddress,
        body=body,
        email='',
        phone=''
    )
    
    msg = Message(
        title, sender=mail_sender, recipients=recipients, html=msg_html)
    mail.send(msg)