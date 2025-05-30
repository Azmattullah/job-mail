import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


load_dotenv()

class SendEmailClass:
    def __init__(self, sender_email, receiver_email, subject, body, pdf_path):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject
        self.body = body
        self.pdf_path = pdf_path
        self.smtp_server = "smtp.mail.yahoo.com"
        self.smtp_port = 587
        self.app_password = os.getenv("APP_PASSWORD")

    def send_email_fun(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body, 'html'))

        with open(self.pdf_path, "rb") as pdf_file:
            pdf = MIMEApplication(pdf_file.read(), _subtype="pdf")
            pdf.add_header('Content-Disposition', 'attachment', filename=self.pdf_path)
            msg.attach(pdf)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.send_message(msg)
            print("Email sent successfully!")
            server.quit()
        except Exception as e:
            print("Error:", e)
