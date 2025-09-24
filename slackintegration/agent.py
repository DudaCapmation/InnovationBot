import logging

from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .tools import get_initiatives, get_initiative_by_id, create_initiative, update_initiative, delete_initiative, get_status_list
from .authorization import get_permissions
from .tool_mapping import get_role_tools

load_dotenv()

logger = logging.getLogger(__name__)

ADMIN_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system",  "You are an Admin Agent and Chatbot called Innovation Bot with access to system tools."
                    "Use tools only when necessary and feel free to ask the user for clarification if/when needed."
                    "Always reply to the user's message in a polite and professional way. Use markdown for formatting."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

def run_agent(user_instruction: str, slack_client, slack_user_id) -> str:
    """
    If slack_client and slack_user_id are provided, we will:
        1) fetch the Slack user's email
        2) call OutSystems GetPermissions (X-User-Token header with email)
        3) limit tools to role returned
    Otherwise, default to read-only tools (safe fallback).
    """

    user_email = ""
    if slack_client and slack_user_id:
        from .slack_utils import get_slack_user_email
        user_email = get_slack_user_email(client=slack_client, slack_user_id=slack_user_id)

    role = ""
    if user_email:
        try:
            permissions_resp = get_permissions(user_token=user_email)
            if permissions_resp.get("status") == "ok":
                # Returns the user's role
                role = permissions_resp.get("role")
            else:
                # If error
                logger.info("GetPermissions error: %s", permissions_resp.get("message"))
                # Returning message to the user
                return "I couldn't verify your permissions. Please try again later."
        except Exception:
            logger.exception("Failed to call permissions endpoint")
            return "Failed to check permissions. Please try again later."

    tools = get_role_tools(role or "user")

    llm = ChatOpenAI(model="gpt-4o-mini")
    agent = create_tool_calling_agent(llm, tools, prompt=ADMIN_PROMPT)
    executor = AgentExecutor(agent=agent, tools=tools)

    result = executor.invoke({"input": user_instruction})

    return result.get("output") # Gets only the agent output