import csv
import smtplib
from email.message import EmailMessage


class input:
    def __init__(self, SENDER, PASSWORD, SUBJECT, BODY):
        self.SENDER = str(SENDER)
        self.PASSWORD = str(PASSWORD)
        self.SUBJECT = str(SUBJECT)
        self.BODY = str(BODY)

    def csvData(self, FILE, FIRST_NAME, LAST_NAME, EMAIL):
        self.FILE = str(FILE)
        self.FIRST_NAME = str(FIRST_NAME)
        self.LAST_NAME = str(LAST_NAME)
        self.EMAIL = str(EMAIL)

    def send(self):
        with open(self.FILE, 'r') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for data in csvReader:
                self.BODY = self.BODY.format(
                    data[self.FIRST_NAME], data[self.LAST_NAME]
                )
                self.RECEIVER = data[self.EMAIL]

                self.mssg = EmailMessage()
                self.mssg['From'] = self.SENDER
                self.mssg['To'] = self.RECEIVER
                self.mssg['Subject'] = self.SUBJECT
                self.mssg.set_content(self.BODY)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(self.SENDER, self.PASSWORD)
                    server.send_message(self.mssg)
