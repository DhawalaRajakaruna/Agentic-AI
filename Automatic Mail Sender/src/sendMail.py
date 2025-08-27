import base64
from email.mime.text import MIMEText

def sendmail(service,isreply, replyto, resubject, rebody):
    if not isreply:
        print("Not marked as a reply. Mail not sent.")
        return
    message = MIMEText(rebody)
    message['to'] = replyto
    message['subject'] = resubject
    message['from'] = "me"

    #encoding the message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        send_result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        print(f"Reply sent successfully! Message ID: {send_result['id']}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")