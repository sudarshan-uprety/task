import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from utils import env


BOOKING_EMAIL_CONFIG = {
    'host': env.EMAIL_HOST,
    'port': env.EMAIL_PORT,
    'username': env.EMAIL_HOST_USER,
    'password': env.EMAIL_HOST_PASSWORD,
    'use_tls': True,
    'from_email': env.EMAIL_HOST_USER,
}


def send_booking_confirmation(booking):
    subject = f'Booking Confirmation - {booking.event.title}'

    context = {
        'user': booking.user.email,
        'event': booking.event.title,
        'booking': booking,
        'booking_date': booking.booking_date.strftime('%B %d, %Y'),
        'event_date': booking.event.date.strftime('%B %d, %Y'),
    }

    html_message = render_to_string('booking_mail.html', context)
    plain_message = strip_tags(html_message)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = BOOKING_EMAIL_CONFIG['from_email']
    msg['To'] = booking.user.email

    msg.attach(MIMEText(plain_message, 'plain'))
    msg.attach(MIMEText(html_message, 'html'))

    server = smtplib.SMTP(BOOKING_EMAIL_CONFIG['host'], BOOKING_EMAIL_CONFIG['port'])
    server.starttls()
    server.login(BOOKING_EMAIL_CONFIG['username'], BOOKING_EMAIL_CONFIG['password'])

    server.send_message(msg)
    server.quit()
