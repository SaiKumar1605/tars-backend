import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

def send_slack_message(channel: str, text: str):
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        return {"ok": True, "ts": response["ts"]}
    except SlackApiError as e:
        return {"ok": False, "error": e.response["error"]}
