from googleapiclient.discovery import build
from google_api.auth import get_google_creds

def read_latest_emails(max_results=5):
    creds = get_google_creds()
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])
    
    email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        subject = next((h["value"] for h in msg_data["payload"]["headers"] if h["name"] == "Subject"), "No Subject")
        email_list.append(subject)
    return email_list
