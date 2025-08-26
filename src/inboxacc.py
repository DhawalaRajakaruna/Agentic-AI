
from email.utils import parseaddr
import base64

emailList=["dhawalabiz2002@gmail.com"]




def get_email_body(payload, headers):
    """
    Extracts the email body. If the email is a reply, returns only the latest reply text.
    headers: list of headers from the message payload
    """
    # Determine if email is a reply
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "")
    in_reply_to = next((h['value'] for h in headers if h['name'] == 'In-Reply-To'), None)
    is_reply = subject.lower().startswith("re:") or in_reply_to is not None

    # Get raw email body
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
            elif part['mimeType'] == 'text/html':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
    else:
        data = payload['body'].get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')

    # If it's a reply, extract only the last reply
    if is_reply:
        body = extract_last_reply(body)

    return body


def extract_last_reply(body):
    """
    Extracts only the latest reply text by splitting on common reply markers
    like lines starting with '>' or 'On <date>, <sender> wrote:'
    """
    split_markers = ["\n>", "\nOn", "\nFrom:", "\nSent:"]
    for marker in split_markers:
        if marker in body:
            body = body.split(marker)[0].strip()
    return body


#just commnet
#=====================================================================

def read_inbox(service):
    # List unread messages
    results = service.users().messages().list(
                        userId='me', 
                        labelIds=['INBOX'], 
                        q="is:unread"
                        ).execute()
    
    messages = results.get('messages', [])

    if not messages:
        print("No new emails.")
    else:
        for msg in messages:
            # Get the message details
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload.get("headers")
            
            body = get_email_body(payload, headers)

            subject = sender = None

            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            # Email snippet (preview)
            snippet = txt.get('snippet')
            _, email_address = parseaddr(sender) 

            if email_address in emailList:
                return subject.lower().startswith("re:"), email_address, subject, body
    
    # If no matching email is found, return None values
    return None, None, None, None


