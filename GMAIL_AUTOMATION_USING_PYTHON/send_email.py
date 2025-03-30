from dotenv import load_dotenv
load_dotenv("./a.env")

import os
from email.message import EmailMessage
import ssl 
"""Provides secure communication by creating SSL (Secure Sockets Layer) contexts. This ensures your connection to the SMTP server is encrypted."""
import smtplib
"""A Python library used for sending emails through the SMTP (Simple Mail Transfer Protocol) server."""

email_sender="anshumansamantapc@gmail.com"
email_password=os.environ.get("EMAIL_PASSWORD")  #environment variable ,,EMAIL_PASSWORD , a variable--FOR HIDING THE PASSWORD
#email_password="irzcvdqnjpsihgxe"

"""email_reciever="itisanshu@gmail.com"""

email_reciever=input("enter the recieving email..")


subject=input("Enter the subject")
body=input("Enter the body..")
for i in range(10):
    em=EmailMessage()
    em["From"]=email_sender
    em["To"]=email_reciever
    em["Subject"]=subject
    em.set_content(body)

    context=ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, local_hostname="localhost") as smtp:
            smtp.set_debuglevel(1) 
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_reciever, em.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication error:", e)
    except smtplib.SMTPConnectError as e:
        print("Connection error:", e)
    except Exception as e:
        print("An error occurred:", e)