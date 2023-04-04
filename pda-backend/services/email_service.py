import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content



# Send an HTTP POST request to /mail/send
def send_email():
    api_key = os.environ.get('SENDGRID_API_KEY')
    api_key = os.environ.get('SENDGRID_API_KEY')
    sg = sendgrid.SendGridAPIClient(api_key)
    from_email = Email("jarvis@tinahoeflich.de")  # Change to your verified sender
    to_email = To("tina.h.hoeflich@gmail.com")  # Change to your recipient
    subject = "Jarvis asking for your support"
    content = Content("text/plain", "Hi there, \n \nyour friend may need someone to cheer him up :) \nCan you help me out with this? \n \nThanks, \n Jarvis")
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
