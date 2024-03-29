from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread


def send_async_email(app, msg):
    # This function will run in the background thread.
    # When the process completes the thread will end
    # and clean itself up.
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
