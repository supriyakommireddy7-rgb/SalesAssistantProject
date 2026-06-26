import os
import base64
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticates using credentials.json, saving/reusing token.json."""
        creds = None
        token_path = os.path.join(os.path.dirname(__file__), '..', 'token.json')
        creds_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')

        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception as e:
                print(f"Error reading token.json: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing expired token: {e}")
                    creds = None # Force re-auth
            
            if not creds or not creds.valid:
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(
                        "credentials.json not found! Please place your Gmail OAuth "
                        "credentials.json in the backend/ folder."
                    )
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    raise RuntimeError(f"Gmail OAuth Authentication failed: {e}")

            if creds:
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

        self.creds = creds
        if self.creds:
            try:
                self.service = build('gmail', 'v1', credentials=self.creds)
            except Exception as e:
                raise RuntimeError(f"Failed to build Gmail service: {e}")
        else:
            raise RuntimeError("Failed to authenticate with Gmail.")

    def get_unread_emails(self):
        """Fetches unread emails, ignoring spam, trash, and sent emails."""
        if not self.service:
            raise RuntimeError("Gmail service not initialized.")
        
        try:
            # Strictly ignore SPAM, TRASH, and SENT
            query = "is:unread -label:SPAM -label:TRASH -label:SENT"
            results = self.service.users().messages().list(
                userId='me', q=query
            ).execute()
            
            messages = results.get('messages', [])
            email_data = []
            
            for msg in messages:
                msg_id = msg['id']
                try:
                    message = self.service.users().messages().get(
                        userId='me', id=msg_id, format='full'
                    ).execute()
                except Exception as e:
                    print(f"Failed to fetch message details for {msg_id}: {e}")
                    continue
                
                headers = message['payload'].get('headers', [])
                
                subject = "No Subject"
                from_header = "Unknown Sender"
                message_id = ""
                
                for header in headers:
                    if header['name'] == 'Subject':
                        subject = header['value']
                    elif header['name'] == 'From':
                        from_header = header['value']
                    elif header['name'] == 'Message-ID':
                        message_id = header['value']
                
                # Parse sender name and email
                sender_name = from_header
                sender_email = from_header
                match = re.match(r"(.*)<(.*)>", from_header)
                if match:
                    sender_name = match.group(1).strip().strip('"')
                    sender_email = match.group(2).strip()

                body = self._get_email_body(message['payload'])
                
                email_data.append({
                    'gmail_msg_id': msg_id,
                    'gmail_thread_id': message['threadId'],
                    'message_id': message_id,
                    'subject': subject,
                    'sender_name': sender_name,
                    'sender_email': sender_email,
                    'body': body
                })
            return email_data
        except Exception as e:
            raise RuntimeError(f"Error fetching emails: {e}")

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

    def send_reply(self, thread_id, to, subject, message_text, in_reply_to_message_id=None):
        """Replies to a thread, using threadId so replies group properly in Gmail."""
        if not self.service:
            raise RuntimeError("Gmail service not initialized.")
            
        try:
            message = MIMEText(message_text)
            message['to'] = to
            message['subject'] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
            
            # Standard headers to ensure proper threading
            if in_reply_to_message_id:
                message['In-Reply-To'] = in_reply_to_message_id
                message['References'] = in_reply_to_message_id
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            body = {'raw': raw_message, 'threadId': thread_id}
            
            self.service.users().messages().send(
                userId='me',
                body=body
            ).execute()
            
            return True
        except Exception as e:
            raise RuntimeError(f"Error sending reply: {e}")
            
    def mark_as_read(self, msg_id):
        """Removes the UNREAD label from a message."""
        if not self.service:
            raise RuntimeError("Gmail service not initialized.")
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            raise RuntimeError(f"Error marking read for {msg_id}: {e}")
