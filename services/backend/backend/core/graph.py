from langgraph.graph import StateGraph, END
from backend.core.state import AgentState
from backend.core.nodes import call_model, execute_tools, should_continue


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
agent_executor = workflow.compile()

# agent_executor.get_graph().draw("langgraph_chart.png", prog="dot")
