import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_RECIPIENTS = os.getenv("ALERT_RECIPIENTS", "").split(",")

def send_alert(subject, body):
    msg = MIMEMultipart()
    msg["FROM"] = EMAIL_USER
    msg["To"] = ", ".join(ALERT_RECIPIENTS)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, ALERT_RECIPIENTS, msg.as_string())
        print(f"Alert sent to: {ALERT_RECIPIENTS}")
    except Exception as e:
        print(f"Failed to send alert: {e}")    