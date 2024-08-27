from django.core.mail import EmailMessage


import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(subject,message,from_email,to_email):
        email = EmailMessage(
            subject=subject, body=message,from_email=from_email,to=[to_email])
        email.content_subtype = "html"
        EmailThread(email).start()