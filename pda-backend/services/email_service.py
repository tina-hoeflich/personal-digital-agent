import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content


def send_email(from_email: str, to_email: str, subject: str, content: str) -> Mail:
    sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = subject
    content = Content("text/plain", content)
    mail = Mail(from_email, to_email, subject, content)

    sg.send(mail)
    return mail
