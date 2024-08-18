import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

from dotenv import load_dotenv

load_dotenv()

def write_email(email_details, filenames=None, is_html=False):
    msg = MIMEMultipart()
    msg.attach(MIMEText(f"""
                <p>{email_details['body']}</p><br>
                <p style='font-family: Courier, sans-serif; font-size: 10px;'>
                Report fetched {formatdate(localtime=True)} and was processed in {email_details['elapsed']:.3f} seconds.<br>
                Source Code: <a href='https://github.com/wlinds/notion-summarizer'>wlinds/notion-summarizer</a></p>""", 'html' if is_html else 'plain'))
    
    msg['From'] = email_details['sender']
    msg['To'] = email_details['receiver']
    msg['Subject'] = f"{ email_details['subject']} {email_details['week']}"
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

    if email_details['sender'][-9::] == 'gmail.com':
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_details['sender'], os.getenv('EMAIL_APP_PASSWORD'))
            smtp.send_message(msg)
            return 1
    else:
        print("Your email provider is not supported. Check send_email.py to configure SSL")
        
    return 0

if __name__ == "__main__":
    pass