from typing import Literal

from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langsmith.run_helpers import traceable

from ask_f1_agent.agent.state import AgentState
from ask_f1_agent.config import CFG
from ask_f1_agent.services.f1_mcp import mcp_manager
from ask_f1_agent.services.llm import llm
from ask_f1_agent.tools.chroma_tool import document_search
from ask_f1_agent.utils.logger import logger
from ask_f1_agent.utils.utils import get_package_root

with open(get_package_root(CFG.package_name) / CFG.sys_prompt_path, "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()

LLM_WITH_TOOLS = None


def _llm_with_tools():
    global LLM_WITH_TOOLS
    if LLM_WITH_TOOLS is None:
        # Bind the tools to the LLM
        LLM_WITH_TOOLS = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ) | llm.bind_tools(
            tools=[document_search] + mcp_manager.tools,
        )
    return LLM_WITH_TOOLS


# LLM call node
@traceable(run_type="chain", name="Call LLM for Decision")
async def call_model(state: AgentState, config: RunnableConfig) -> dict:
    """Invokes the LLM to either generate a response or request a tool call."""
    messages = state["messages"]

    response = await _llm_with_tools().ainvoke(messages, config)

    return {"messages": [response]}


# Tool execution node
@traceable(run_type="tool", name="Execute Agent Tools")
async def execute_tools(state: AgentState) -> dict:
    """Executes the tool calls requested by the LLM."""
    last_message = state["messages"][-1]

    tool_results = []

    # Map of tool names to actual callable tool objects
    tools = {"document_search": document_search}
    mcp_tool_map = {tool.name: tool for tool in mcp_manager.tools}
    tools.update(mcp_tool_map)

    # Iterate over tool calls requested by the LLM
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        if tool_name not in tools:
            logger.error(f"Requested tool '{tool_name}' is not recognized.")
            result = f"Error: Unknown tool '{tool_name}'"
        else:
            try:
                # Execute the tool function with the provided arguments
                result = await tools[tool_name].ainvoke(tool_args)
            except Exception as e:
                logger.error(f"Error executing tool '{tool_name}': {e}")
                result = f"Error executing tool '{tool_name}': {str(e)}"

        # Add the ToolMessage back to the history for the LLM to see
        tool_results.append(ToolMessage(content=str(result), tool_call_id=tool_call_id))

    return {"messages": tool_results}


# Conditional routing function
def should_continue(state: AgentState) -> Literal["tool", "final_answer"]:
    """Decides if the graph should loop back to call_model (tool requested) or stop."""
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tool"
    return "final_answer"
