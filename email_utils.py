import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email, subject, message):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    email = MIMEText(message)

    email["Subject"] = subject
    email["From"] = sender_email
    email["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            sender_email,
            sender_password
        )

        server.sendmail(
            sender_email,
            to_email,
            email.as_string()
        )