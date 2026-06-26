import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    pass
            elif os.path.exists('credentials.json'):
                try:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception:
                    pass
            if creds:
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        self.creds = creds
        if self.creds:
            self.service = build('gmail', 'v1', credentials=self.creds)

    def get_unread_emails(self):
        if not self.service:
            return []
        
        try:
            results = self.service.users().messages().list(userId='me', labelIds=['UNREAD'], q="is:unread").execute()
            messages = results.get('messages', [])
            email_data = []
            
            for msg in messages:
                msg_id = msg['id']
                message = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                
                headers = message['payload'].get('headers', [])
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
                
                body = self._get_email_body(message['payload'])
                
                email_data.append({
                    'gmail_msg_id': msg_id,
                    'gmail_thread_id': message['threadId'],
                    'subject': subject,
                    'sender': sender,
                    'body': body
                })
            return email_data
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []

    def _get_email_body(self, payload):
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode('utf-8')
                elif 'parts' in part:
                    body += self._get_email_body(part)
        else:
            data = payload['body'].get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        return body

    def send_reply(self, thread_id, to, subject, message_text):
        if not self.service:
            return False
            
        try:
            from email.mime.text import MIMEText
            message = MIMEText(message_text)
            message['to'] = to
            message['subject'] = subject if subject.startswith("Re:") else f"Re: {subject}"
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message, 'threadId': thread_id}
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error sending reply: {e}")
            return False
            
    def mark_as_read(self, msg_id):
        if not self.service:
            return False
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            print(f"Error marking read: {e}")
            return False
