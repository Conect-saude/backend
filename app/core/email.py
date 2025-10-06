# app/core/email.py
import smtplib
from email.message import EmailMessage
from app.core.config import settings


def send_email(to_email: str, subject: str, html: str):
    if not settings.SMTP_HOST or not settings.SMTP_FROM:
        # Fallback: loga no console em desenvolvimento
        print("[EMAIL:DEV] To:", to_email)
        print("[EMAIL:DEV] Subject:", subject)
        print("[EMAIL:DEV] HTML:\n", html)
        return
    
    msg = EmailMessage()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(html, subtype="html")


    with smtplib.SMTP(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as s:
        if settings.SMTP_USER:
            s.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        s.send_message(msg)