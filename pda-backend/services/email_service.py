import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content


def send_email(from_email: str, to_email: str, subject: str, content: str) -> Mail:
    """
    Method that sends an email to the given email address with the given subject and content
    :param from_email: the email address of the sender
    :param to_email: the email address of the receiver
    :param subject: the subject of the email
    :param content: the content of the email
    :return: the mail object
    """
    sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = subject
    content = Content("text/plain", content)
    mail = Mail(from_email, to_email, subject, content)

    sg.send(mail)
    return mail
