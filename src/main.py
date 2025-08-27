import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from authentication import gmail_authenticate
from inboxacc import read_inbox
#from mailgeneration import createmail
from replygeminai import Generatemail
from sendMail import sendmail

# Authentication and service creation
service = gmail_authenticate()

# Access the inbox
isaReply, email_address, subject, body = read_inbox(service)
reply = None
if email_address is None:
    print("No relevant unread emails found from specified senders.")
else:
    #resubject,reply = createmail(email_address, subject, body)
    isreply, replyto, resubject, rebody=Generatemail(email_address, subject, body)
    print(isreply)
    print(replyto)
    print(resubject)
    print(rebody)
    print("="*50)

#Sending the reply

