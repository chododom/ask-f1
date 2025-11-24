from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from ask_f1_agent.agent.nodes import call_model, execute_tools, should_continue
from ask_f1_agent.agent.state import AgentState

# In-memory storage of conversation history
memory = MemorySaver()


def build_graph():
    """
    Uses nodes to create the agent execution graph.
    """
    workflow = StateGraph(AgentState)

    # Graph nodes
    workflow.add_node("llm", call_model)
    workflow.add_node("tools", execute_tools)

    # Graph edges
    workflow.set_entry_point("llm")
    workflow.add_conditional_edges(
        "llm",
        should_continue,
        {
            # If should_continue returns "tool", go to the "tools" node
            "tool": "tools",
            # If should_continue returns "final_answer", stop and return the result
            "final_answer": END,
        },
    )
    workflow.add_edge("tools", "llm")

    # Compile the graph into an executable agent
    agent_executor = workflow.compile(checkpointer=memory)

    # agent_executor.get_graph().draw("langgraph_chart.png", prog="dot")

    return agent_executor


agent_executor = build_graph()
