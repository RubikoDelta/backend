import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv


def sendMail(html, subject, to):
    msg = MIMEMultipart('alternave')
    msg['Subject'] = subject
    msg['From'] = os.getenv("SMTP_USER")
    msg['To'] = to

    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"))
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_USER"), to, msg.as_string())
        server.quit()
    except smtplib.SMTPResponseException as e:
        print("error envio mail")
