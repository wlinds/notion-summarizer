import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

from dotenv import load_dotenv

load_dotenv()

def write_email(sender, receiver, subject, body, filenames=None, is_html=False):
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
    
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    if isinstance(filenames, str):
        filenames = [filenames]

    if filenames:
        for filename in filenames:
            with open(filename, "rb") as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filename}")
                msg.attach(part)

    if sender[-9::] == 'gmail.com':
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, os.getenv('EMAIL_APP_PASSWORD'))
            smtp.send_message(msg)
            return 1
    else:
        print("Your email provider is not supported. Check send_email.py to configure SSL")
        
    return 0

if __name__ == "__main__":
    pass