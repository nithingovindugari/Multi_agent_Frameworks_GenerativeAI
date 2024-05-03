import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Follow documentation in mailtrap website to get the username and password
# https://mailtrap.io/

load_dotenv()

send_email_declaration = {
    "name": "send_mail",
    "description": "Sends an email using SMTP with a specified subject, body, and recipient.",
    "parameters": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "The subject of the email"
            },
            "body": {
                "type": "string",
                "description": "The body content of the email"
            },
            "to_email": {
                "type": "string",
                "description": "The recipient's email address"
            }
        },
        "required": ["subject", "body", "to_email"]
    },
}




# Function to send mail
def send_mail(subject, body, to_email):
    sender = " Private Person <from@example.com>"
    
    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to_email
    
    # Send the message via our own SMTP server.
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("8064bd9cae3b81", smtp_password)
        server.send_message(message)
        return "Email sent successfully"
    
# Test the function by sending a test email to whatever test email you want to send
# send_mail("Test", "This is a test email", "nit@ai.com")
    
    
    