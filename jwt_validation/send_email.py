# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail




# sender_email = "editoraaron@gmail.com"
# receiver_email = "aaron.aa@me.com"

# def send_email(code):
#   message = Mail(
#       from_email=sender_email,
#       to_emails=receiver_email,
#       subject='Your code',
#       html_content=f'<html><body><p>Hello, your verification code is: {code}</p></body</html>')
#   try:
#       sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#       response = sg.send(message)
#       print(response.status_code)
#       print(response.body)
#       print(response.headers)
#   except Exception as e:
#       print(e)



# #   https://realpython.com/python-send-email/

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

sender_email = "editoraaron@gmail.com"
receiver_email = "editoraaron@gmail.com"
password = "rnmtzlqbujjziika"

message = MIMEMultipart("alternative")
message["Subject"] = "Sign in code"
message["From"] = sender_email
message["To"] = receiver_email



def send_email(code):
  # Create the plain-text and HTML version of your message
  text = """\
  Hi,
  Thank you.
  """

  html = f"""\
  <html>
    <body>
      <p>
        Hello, your verification code is: {code}
      </p>
    </body>
  </html>
  """

  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      try:
          server.login(sender_email, password)
          server.sendmail(sender_email, receiver_email, message.as_string())
      except Exception as ex:
          print(ex)

