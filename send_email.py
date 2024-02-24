import smtplib
class EmailSender:
    receiver_emails = ['20euit016@skcet.ac.in', '20euit060@skcet.ac.in', '20euit031@skcet.ac.in', '20euit030@skcet.ac.in', '20euit029@skcet.ac.in']
    def __init__(self, sender_email, password):
        self.sender_email = sender_email
        self.password = password
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.sender_email, self.password)

    def send_email(self, subject, body):
        for receiver_email in EmailSender.receiver_emails:
            message = f"Subject: {subject}\n\n{body}"
            self.server.sendmail(self.sender_email, receiver_email, message)
        print("Mail Sent")
        