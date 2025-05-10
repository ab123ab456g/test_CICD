import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import sys

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_email(subject, body):
    creds = Credentials(
        token=None,
        refresh_token=os.environ['GMAIL_REFRESH_TOKEN'],
        client_id=os.environ['GMAIL_CLIENT_ID'],
        client_secret=os.environ['GMAIL_CLIENT_SECRET'],
        token_uri='https://oauth2.googleapis.com/token'
    )
    service = build('gmail', 'v1', credentials=creds)
    message = create_message(
        sender="ab123ab456g@gmail.com",
        to="ab123ab456g@gmail.com",
        subject=subject,
        message_text=body
    )
    send_message = service.users().messages().send(userId="me", body=message).execute()
    print(f"訊息已發送，ID: {send_message['id']}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python send_email.py \"主旨\" \"內文\"")
        sys.exit(1)

    subject = sys.argv[1]
    body = sys.argv[2]
    send_email(subject, body)
