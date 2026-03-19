import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
# 'readonly' allows you to read messages but not delete or send them.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def list_recent_messages():
    service = get_gmail_service()
    # Fetch the 10 most recent messages
    results = service.users().messages().list(userId='me', maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print('Recent Messages:')
        for msg in messages:
            message_id = msg['id']
            data = get_message_content(message_id)
            print(f"- Snippet: {data}")
            # detail = service.users().messages().get(userId='me', id=msg['id']).execute()
            # # Convert to ascii, ignoring characters the terminal can't print
            # safe_snippet = detail['snippet'].encode('ascii', errors='ignore').decode('ascii')
            # print(f"- Snippet: {safe_snippet}")

def list_filtered_messages(query_string=None):
    """
    Lists messages matching a specific query.
    Example query_string: 'from:someone@gmail.com is:unread'
    """
    service = get_gmail_service()
    
    # Use 'q' to filter results. MaxResults is set to 10 here for efficiency.
    results = service.users().messages().list(
        userId='me', 
        q=query_string, 
        maxResults=1
    ).execute()
    
    messages = results.get('messages', [])

    if not messages:
        print(f"No messages found for query: '{query_string}'")
    else:
        print(f"Matching Messages for '{query_string}':")
        for msg in messages:

            message_id = msg['id']
            data = get_message_content(message_id)
            print(f"- Snippet: {data}")

            # # Fetch the full message details (Subject and Snippet)
            # detail = service.users().messages().get(userId='me', id=msg['id']).execute()
            
            # # Extract Subject from headers
            # headers = detail.get('payload', {}).get('headers', [])
            # subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            
            # print(f"--- \nSubject: {subject}\nSnippet: {detail['snippet']}")

# Example usages:
# list_filtered_messages('from:avi@dailydoseofds.com')
# list_filtered_messages('is:unread "action required"')

def get_message_content(message_id):
    """
    Fetches and decodes the full body text of a specific message ID.
    Can be used in the above methods to get the full message content.
    """
    service = get_gmail_service()
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    payload = message.get('payload', {})
    parts = payload.get('parts', [])
    
    body = ""

    # Emails can be simple or multipart (text + html)
    if not parts:
        # Simple email with no parts
        data = payload.get('body', {}).get('data', '')
    else:
        # Multipart email: usually the first part (index 0) is plain text
        # But we'll look for 'text/plain' specifically to be safe
        data = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part.get('body', {}).get('data', '')
                break

    if data:
        # Decode from URL-safe Base64
        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
        body = decoded_data

    return body
    
if __name__ == '__main__':
    print('start')
    # list_recent_messages()
    list_filtered_messages('from:avi@dailydoseofds.com')