from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .tools import get_initiatives, get_initiative_by_id, create_initiative, update_initiative, delete_initiative, get_status_list

load_dotenv()

ADMIN_PROMPT = ChatPromptTemplate.from_template(
    "You are an Admin Agent and Chatbot called Innovation Bot with access to system tools."
    "Use tools only when necessary and feel free to ask the user for clarification if/when needed."
    "Always reply to the user's message in a polite and professional way."
    "User's message: {input}"
    "{agent_scratchpad}"
)

def run_agent(user_instruction: str) -> str:

    llm = ChatOpenAI(model="gpt-4o-mini")
    tools = [get_initiatives, get_initiative_by_id, create_initiative, update_initiative, delete_initiative, get_status_list]

    agent = create_tool_calling_agent(llm, tools, prompt=ADMIN_PROMPT)
    executor = AgentExecutor(agent=agent, tools=tools)

    result = executor.invoke({"input": user_instruction})

    return str(result)