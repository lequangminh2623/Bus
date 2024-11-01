from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import json

# Load credentials and tokens
with open('C:\\Users\\MINH\\Documents\\Zalo_Received_Files\\OUBus\\OUBusUI\\credentials.json') as creds_file:
    credentials_info = json.load(creds_file)['installed']
    
with open(r'C:\Users\MINH\Documents\Zalo_Received_Files\OUBus\OUBusApi\busmap\token.json') as token_file:
    token_info = json.load(token_file)

def get_gmail_service():
    creds = Credentials(
        token=token_info['access_token'],
        refresh_token=token_info['refresh_token'],
        token_uri=credentials_info['token_uri'],
        client_id=credentials_info['client_id'],
        client_secret=credentials_info['client_secret']
    )
    return build('gmail', 'v1', credentials=creds)

def create_message(from_address, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = from_address
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(from_address_trip, to_address_trip, time_string):
    try:
        service = get_gmail_service()
        subject = "Trip Details"
        body = f'Starting Address: {from_address_trip}\nEnding Address: {to_address_trip}\nTime: {time_string}'
        to_address = "prolathe633@gmail.com"  # Default recipient address
        message = create_message(from_address_trip, to_address, subject, body)
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message sent. ID: {sent_message['id']}")
        return sent_message['id']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# Usage
