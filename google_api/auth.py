from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar"
]

def get_google_creds():
    creds = None
    # if os.path.exists("token.json"):           #For local
    #     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if os.path.exists("/etc/secrets/token.json"):
        creds = Credentials.from_authorized_user_file("/etc/secrets/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES) #For local
            flow = InstalledAppFlow.from_client_secrets_file("/etc/secrets/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds
