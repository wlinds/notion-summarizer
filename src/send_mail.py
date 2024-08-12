import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

def write_email(sender, receiver, subject, body, filename=None, is_html=False):
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
    

    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    if filename:
        with open(filename, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

    # return sender, msg

    if sender[-9::] == 'gmail.com':
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, os.getenv('EMAIL_APP_PASSWORD'))
            smtp.send_message(msg)
    else:
        print("Your email provider is not supported. Check send_email.py to configure SSL")

if __name__ == "__main__":
    pass