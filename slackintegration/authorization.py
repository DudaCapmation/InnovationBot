import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
OUTSYSYEMS_BASE_URL = os.getenv("OUTSYSYEMS_BASE_URL")

def get_permissions(user_token):
    """
    Call OutSystems GetPermissions endpoint using the user's email as token (X-User-Token header).
    Returns a dict with a JSON.
    Expected successful response example:
    {"status": "ok", "userId": "...", "email":"...","role":"admin"}
    On error, the API should return JSON with status=="error".
    """

    if not user_token:
        raise ValueError("user_token required.")

    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/GetPermissions"
    headers = {"X-User-Token": user_token}

    request = requests.get(url, headers=headers)

    return request.json()
