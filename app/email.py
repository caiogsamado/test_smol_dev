from flask_mail import Message
from flask import current_app as app
from threading import Thread
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_subscription_confirmation_email(user, subscription):
    send_email('[Healthcare Startup] Subscription Confirmation',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=f'Dear {user.name},\n\nYour subscription for {subscription.name} has been confirmed.\n\nThank you for choosing us.\n\nHealthcare Startup Team',
               html_body=f'<p>Dear {user.name},</p><p>Your subscription for {subscription.name} has been confirmed.</p><p>Thank you for choosing us.</p><p>Healthcare Startup Team</p>')

def send_payment_confirmation_email(user, payment):
    send_email('[Healthcare Startup] Payment Confirmation',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=f'Dear {user.name},\n\nYour payment of ${payment.amount} has been received.\n\nThank you for your support.\n\nHealthcare Startup Team',
               html_body=f'<p>Dear {user.name},</p><p>Your payment of ${payment.amount} has been received.</p><p>Thank you for your support.</p><p>Healthcare Startup Team</p>')