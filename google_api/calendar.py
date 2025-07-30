from googleapiclient.discovery import build
from google_api.auth import get_google_creds
from datetime import datetime, timedelta

def list_upcoming_events():
    creds = get_google_creds()
    service = build("calendar", "v3", credentials=creds)

    now = datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary", timeMin=now, maxResults=5, singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    return [f"{e['summary']} at {e['start'].get('dateTime', e['start'].get('date'))}" for e in events]

def create_calendar_event(summary, start_time_str, end_time_str):
    creds = get_google_creds()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "start": {"dateTime": start_time_str, "timeZone": "UTC"},
        "end": {"dateTime": end_time_str, "timeZone": "UTC"}
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    return event.get("htmlLink")
