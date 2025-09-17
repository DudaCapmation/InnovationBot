import os
import re
import threading
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from .agent import run_agent

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
    process_before_response=True
)

def agent_reply(user_text: str, say):
    # General function to get LLM replies

    if not user_text:
        logger.debug("Empty user_text; skipping LLM call.")
        return

    try:
        from .openai_utils import get_openai_response

        # Building prompt here
        system_prompt = ("You are a helpful assistant called Innovation Bot."
                         "Reply to the user's message in a polite and professional way.")

        reply = get_openai_response(message=user_text, system_prompt=system_prompt)
        say(text=reply) # say uses the same channel by default, could change to chat_postMessage
    except Exception as e:
        logger.exception("Failed to get reply or send message.")
        say(text="Sorry, an error has occurred. Try again later.")

def run_agent_background (user_text: str, say, thread_ts: str | None):
    # Runs agent in background

    try:
        reply = run_agent(user_instruction=user_text)
        say(reply, thread_ts=thread_ts)
    except Exception:
        logger.exception("Agent failed.")
        say(text="Sorry, an error has occurred. Try again later.")

@app.event("message")
def handle_direct_messages(logger, event, say):
    # Handles message events

    # Filtering to get direct messages only
    channel_type = event.get("channel_type")
    if channel_type != "im":
        return

    # Ignoring deleted messages or edited messages
    if event.get("subtype") in ("message_deleted", "message_changed"):
        logger.debug(f"Ignoring message subtype: {event.get('subtype')}")
        return

    # Ignoring bot messages
    if event.get("subtype") == "bot_message" or event.get("bot_id"):
        logger.debug("Ignoring bot message")
        return

    user_text = event.get("text")
    user = event.get("user")
    thread = event.get("ts")

    logger.info(f"Direct message from {user}: {user_text}")

    # Start background job and return immediately
    t = threading.Thread(
        target=run_agent_background(user_text=user_text,say=say, thread_ts=thread),
        args=(user_text.strip(), True, say, thread),
        daemon=True,
    )
    t.start()

    # Quick message to user
    say(text="Got it! Working on it!", thread_ts=thread)


@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    # Handles app mentions

    # Ignoring deleted messages or edited messages
    if event.get("subtype") in ("message_deleted", "message_changed"):
        logger.debug(f"Ignoring message subtype: {event.get('subtype')}")
        return

    # Ignoring bot messages
    if event.get("subtype") == "bot_message" or event.get("bot_id"):
        logger.debug("Ignoring bot message")
        return

    user_text = event.get("text")
    channel = event.get("channel")
    user = event.get("user")
    thread = event.get("ts")

    logger.info(f"Mention from {user} in {channel}: {user_text}")

    # Remove mention tokens. If nothing but a mention was sent, the bot will reply with a generic message
    clean_user_text = re.sub(r"<@[\w]+>\s*", "", user_text).strip()

    if not clean_user_text:
        logger.debug("No text after removing mention. Generic message sent.")
        say(text="Hello! How may I assist you today?", thread_ts=thread)
        return

    # Start background job and return immediately
    t = threading.Thread(
        target=run_agent_background(user_text=user_text,say=say, thread_ts=thread),
        args=(user_text.strip(), True, say, thread),
        daemon=True,
    )
    t.start()

    # Quick message to user
    say(text="Got it! Working on it!", thread_ts=thread)


# Expose the Django handler
handler = SlackRequestHandler(app)