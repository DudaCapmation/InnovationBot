import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from marshmallow import ValidationError
from pydantic import ValidationError

from .pydantic_models import Initiative

load_dotenv()

OUTSYSYEMS_BASE_URL = os.getenv("OUTSYSYEMS_BASE_URL")


@tool
def get_initiatives():
    """
    Retrieves a list of all initiatives in the system.
    Returns each initiative with its Id (integer), Name (string), StatusId (integer),
    StartDate (date), EndDate (date), TargetEndDate (date), and Description (string).
    """

    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/GetInitiatives"
    request = requests.get(
        url=url)
    request.raise_for_status()

    return request.json()

@tool
def get_initiative_by_id(initiative_id: int) -> dict:
    """
    Retrieves details of a specific initiative by its Id.
    Expects an integer Id and returns the initiative data if it exists.
    """

    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/GetInitiativeById?InitiativeId={initiative_id}"
    request = requests.get(
        url=url)
    request.raise_for_status()

    return request.json()

@tool
def create_initiative(initiative_id: int = None, name: str = None, status_id: int = None,
                      start_date: str = None, end_date: str = None,
                      target_end_date: str = None, description: str = None):
    """
    Creates a new initiative in the system.
    Expects a dictionary with keys: Id (integer), Name (string), StatusId (integer),
    StartDate (date), EndDate (date), TargetEndDate (date), and Description (string).
    """

    # Data validation
    #try:
    #    initiative = Initiative.model_validate(initiative)
    #except ValidationError as e:
    #    return {"status": "error", "type": "validation", "errors": e.errors()}

    # Building final payload
    json_payload = {
        "Id": initiative_id,
        "Name": name,
        "StatusId": status_id,
        "StartDate": start_date,
        "EndDate": end_date,
        "TargetEndDate": target_end_date,
        "Description": description,
    }

    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/CreateInitiative"

    request = requests.post(
        url=url,
        json=json_payload)
    request.raise_for_status()

    return request.json()

@tool
def update_initiative(initiative_id: int = None, name: str = None, status_id: int = None,
                      start_date: str = None, end_date: str = None,
                      target_end_date: str = None, description: str = None):
    """
    Updates an existing initiative.
    Expects a dictionary with keys: Id (integer), Name (string), StatusId (integer),
    StartDate (date), EndDate (date), TargetEndDate (date), and Description (string).
    """

    # Data validation
    #try:
    #    initiative = Initiative.model_validate(initiative)
    #except ValidationError as e:
    #    return {"status": "error", "type": "validation", "errors": e.errors()}

    # Building final payload
    json_payload = {
        "Id": initiative_id,
        "Name": name,
        "StatusId": status_id,
        "StartDate": start_date,
        "EndDate": end_date,
        "TargetEndDate": target_end_date,
        "Description": description,
    }

    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/UpdateInitiative"

    request = requests.put(
        url=url,
        json=json_payload)
    request.raise_for_status()

    return request.json()

@tool
def delete_initiative(initiative_id: int) -> dict:
    """
    Deletes an existing initiative by its Id.
    Expects an integer Id.
    """

    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/DeleteInitiative?InitiativeId={initiative_id}"
    request = requests.get(
        url=url)
    request.raise_for_status()

    return request.json()

@tool
def get_status_list():
    """
    Returns the list of possible initiative statuses.
    The list includes: Pending, In Progress, Completed, Canceled.
    """

    url = f"{OUTSYSYEMS_BASE_URL}/InnovationInitiatives_CS/rest/InnovationApp/GetStatusList"
    request = requests.get(
        url=url)
    request.raise_for_status()

    return request.json()