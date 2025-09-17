import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic_models import Initiative

load_dotenv()

OUTSYSYEMS_BASE_URL = os.getenv("OUTSYSYEMS_BASE_URL")


@tool
def get_initiatives():
    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/GetInitiatives"
    request = requests.post(
        url=url)
    request.raise_for_status()

    return request.json()

@tool
def get_initiative_by_id(initiative_id: int) -> dict:
    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/GetInitiativeById?InitiativeId={initiative_id}"
    request = requests.post(
        url=url)
    request.raise_for_status()

    return request.json()

@tool
def create_initiative(initiative: dict):
    # Data validation
    initiative = Initiative.model_validate(initiative)

    # Building final payload
    json_payload = initiative.model_dump(by_alias=True)
    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/CreateInitiative"

    request = requests.post(
        url=url,
        json=json_payload)
    request.raise_for_status()

    return request.json()

@tool
def update_initiative(initiative: dict):
    # Data validation
    initiative = Initiative.model_validate(initiative)

    # Building final payload
    json_payload = initiative.model_dump(by_alias=True)
    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/UpdateInitiative"

    request = requests.post(
        url=url,
        json=json_payload)
    request.raise_for_status()

    return request.json()

@tool
def delete_initiative(initiative_id: int) -> dict:
    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/DeleteInitiative?InitiativeId={initiative_id}"
    request = requests.post(
        url=url)
    request.raise_for_status()

    return request.json()

@tool
def get_status_list():
    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/GetStatusList"
    request = requests.post(
        url=url)
    request.raise_for_status()

    return request.json()