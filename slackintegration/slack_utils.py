import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(signing_secret=os.getenv("SLACK_SIGNING_SECRET "))

def send_message(channel: str, text: str) -> dict:
    # Sends a message to Slack (channel or user ID). Returns slack response dict.

    try:
        response = client.chat_postMessage(channel=channel, text=text)
        return response.data
    except SlackApiError as e:
        raise

def verify_slack_request(raw_body: bytes, headers: dict) -> bool:
    # Return True if Slack signature verification passes. "headers" should be request.headers

    return verifier.is_valid_request(raw_body,headers)