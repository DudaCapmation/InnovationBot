import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler

load_dotenv()

logger = logging.getLogger(__name__)

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET "),
)

@app.event("message")
def handle_messages(logger, event, say):
    # Handles message events

    user_text = event.get("text")
    channel = event.get("channel")
    user = event.get("user")

    logger.info(f"Message from {user} in {channel}: {user_text}")

    # LLM reply
    try:
        from .openai_utils import get_openai_response

        # Building prompt here temporarily
        prompt = "You are a helpful assistant called Innovation Bot. Reply to the user's message in a polite and professional way."
        reply = get_openai_response(user_text, prompt)
        say(text=reply) # say uses the same channel by default, could change to chat_postMessage
    except Exception as e:
        logger.exception("Failed to get reply or send message.")
        say(text="Sorry, an error has occurred. Try again later.")


# Expose the Django handler
handler = SlackRequestHandler(app)