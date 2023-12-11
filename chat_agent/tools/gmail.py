##
# ADD TO .env:
# GMAIL_CREDENTIALS_FILE = "gmail_credentials.json"
##

# mostly from https://thepythoncode.com/article/use-gmail-api-in-python


import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
from dotenv import load_dotenv


load_dotenv()

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']

gmail_credentials_file = os.getenv('GMAIL_CREDENTIALS_FILE')
gmail_token_file = "gmail_token.pickle"


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(gmail_token_file):
        with open(gmail_token_file, "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                gmail_credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(gmail_token_file, "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


# get the Gmail API service
service = gmail_authenticate()


def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    fp = open(filename, 'rb')
    if main_type == 'text':
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
    elif main_type == 'image':
        msg = MIMEImage(fp.read(), _subtype=sub_type)
    elif main_type == 'audio':
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
    else:
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
    fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)


def build_message(destination, subject, body, attachments=[], message_id=None, thread_id=None):
    message = MIMEMultipart()
    message.attach(MIMEText(body))
    message['to'] = destination
    message['from'] = "me"
    message['subject'] = subject
    if message_id:
        message['In-Reply-To'] = message_id
        message['References'] = message_id

    if attachments:
        for filename in attachments:
            add_attachment(message, filename)
    message = {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    if thread_id:
        message['threadId'] = thread_id

    return message


def send_message(service, destination, subject, body, attachments=[], message_id=None, thread_id=None):
    return service.users().messages().send(
        userId="me",
        body=build_message(destination, subject, body,
                           attachments, message_id, thread_id)
    ).execute()


def search_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(
            userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


def parse_parts(service, parts):
    """
    Utility function that parses the content of an email partition
    """
    output = ""
    if parts:
        for part in parts:
            mime_type = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                output += parse_parts(service, part.get("parts")) + "\n"
            # ignores attachments, only download text
            if mime_type == "text/plain" and data:
                # if the email part is text plain
                output += urlsafe_b64decode(data).decode() + "\n"
    return output


def read_message(service, id):
    msg = service.users().messages().get(
        userId='me', id=id, format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")

    email = {
        "from": None,
        "to": None,
        "subject": None,
        "date": None,
        "content": None,
        "message-id": None
    }

    for header in (headers or []):
        name = header.get("name").lower()
        if name in ['from', 'to', 'subject', 'date', 'message-id']:
            email[name] = header.get("value")

    email['content'] = parse_parts(service, parts)
    if email['content'].strip() == "":
        email['content'] = "No plain text content"

    return email


def mark_as_read(service, ids):
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': ids if isinstance(ids, list) else [ids],
            'removeLabelIds': ['UNREAD']
        }
    ).execute()


def email_to_string(id, email, thread_id=None, with_content=False):
    email_string = f"EMAIL\nGmail id: {id}\nMessage id: {email['message-id']}\nDate: {email['date']}\nFrom: {email['from']}\nTo: {email['to']}\nSubject: {email['subject']}\n"
    if thread_id:
        email_string += f"Thread id: {thread_id}\n"
    if with_content:
        email_string += f"Content: {email['content']}\nEND EMAIL\n\n"
    else:
        email_string += "\n"
    return email_string


async def mark_email_as_read(agent, id):
    mark_as_read(service, id)
    return f"Email {id} marked as read"

async def search_emails(agent, query):
    messages = search_messages(service, query)
    messages = messages[:20]
    messages.reverse()
    output = "EMAILS FOUND WITH QUERY '{query}' (maximum 20 results):\n\n"
    # loop through with index
    for message in messages:
        email = read_message(service, message['id'])
        output += email_to_string(message['id'],
                                  email, thread_id=message['threadId'])
    if len(messages) == 0:
        output += "No emails\n"
    else:
        output += f"Found {len(messages)} emails\n"

    return output


async def send_email(agent, destination, subject, body, attachments=[], message_id=None, thread_id=None):
    send_message(service, destination, subject, body,
                 attachments, message_id, thread_id)
    return f"Email sent to {destination} with subject {subject}"


async def read_email(agent, id):
    message = read_message(service, id)
    return email_to_string(id, message, with_content=True)


tool_read_email = {
    "info": {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read an email from Gmail",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The gmail id of the email to read",
                    }
                },
                "required": ["id"],
            },
        }
    },
    "function": read_email,
}

tool_send_email = {
    "info": {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email with Gmail",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "The destination email address",
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject of the email",
                    },
                    "body": {
                        "type": "string",
                        "description": "The body of the email",
                    },
                    "attachments": {
                        "type": "array",
                        "description": "A list of file paths to attach to the email, relative to the current working directory",
                        "items": {
                            "type": "string",
                        },
                    },
                    "message_id": {
                        "type": "string",
                        "description": "The message id of the email to reply to (ALWAYS INCLUDE THIS WHEN REPLYING TO AN EMAIL)",
                    },
                    "thread_id": {
                        "type": "string",
                        "description": "The thread id of the email to reply to (ALWAYS INCLUDE THIS WHEN REPLYING TO AN EMAIL)",
                    },
                },
                "required": ["destination", "subject", "body"],
            },
        }
    },
    "function": send_email,
}


tool_search_emails = {
    "info": {
        "type": "function",
        "function": {
            "name": "search_emails",
            "description": "Search emails from Gmail (returns maximum 20 results, with from, to, subject, date, message id, and thread id, message id and thread id can be used to read an email or reply to an email, they never need to be told to the user)",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for, supports Gmail search operators (e.g. use 'is:unread' to search for unread emails)",
                    }
                },
                "required": ["query"],
            },
        }
    },
    "function": search_emails,
}

tool_mark_email_as_read = {
    "info": {
        "type": "function",
        "function": {
            "name": "mark_email_as_read",
            "description": "Mark an email as read in Gmail",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The gmail id of the email to mark as read",
                    }
                },
                "required": ["id"],
            },
        }
    },
    "function": mark_email_as_read,
}
