import os
import logging
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

load_dotenv()

logger = logging.getLogger(__name__)

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

def get_slack_user_email(client, slack_user_id):
    try:
        response = client.users_info(user=slack_user_id)
        if response.get("ok"):
            profile = response["user"].get("profile", {})
            email = profile.get("email")
            if not email:
                logger.info("users_info returned no email for user %s", slack_user_id)
            return email
        logger.warning("users_info failed: %s", response)
    except Exception:
        logger.exception("Failed to call users_info for %s", slack_user_id)
    return None