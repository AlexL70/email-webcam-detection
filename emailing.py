import os
import smtplib as smtp
import imghdr
from email.message import EmailMessage

EMAIL = 'alexander.levinson.70@gmail.com'
PASSWORD = os.environ.get('APP2_PORTFOLIO_EMAIL_PASSWORD')


def send_email(image_path: str):
    email_message = EmailMessage()
    email_message['Subject'] = 'Intruder Alert!'
    email_message.set_content(
        'An intruder was detected! Please see the image attached.')
    with open(image_path, 'rb') as image:
        data = image.read()
    email_message.add_attachment(data, maintype='image',
                                 subtype=imghdr.what(None, data), filename=image.name)
    gmail = smtp.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL, PASSWORD)
    gmail.sendmail(EMAIL, EMAIL, email_message.as_string())
    gmail.quit()
    print(f"Email was sent with {image_path} image.")


if __name__ == '__main__':
    send_email('images/intruder_00000001.png')
