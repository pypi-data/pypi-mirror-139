import smtplib
from email.message import EmailMessage


class input:
    def __init__(self, SENDER, PASSWORD, RECEIVER, SUBJECT, BODY):
        self.SENDER = str(SENDER)
        self.PASSWORD = str(PASSWORD)
        self.RECEIVER = str(RECEIVER)
        self.SUBJECT = str(SUBJECT)
        self.BODY = str(BODY)

    def send(self):
        self.mssg = EmailMessage()
        self.mssg['From'] = self.SENDER
        self.mssg['To'] = self.RECEIVER
        self.mssg['Subject'] = self.SUBJECT
        self.mssg.set_content(self.BODY)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(self.SENDER, self.PASSWORD)
            server.send_message(self.mssg)
