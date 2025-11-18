from langchain_mcp_adapters.client import MultiServerMCPClient


MCP_TOOLS = []


async def fetch_mcp_tools():
    mcp_client = MultiServerMCPClient(
        {
            "fastf1": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    tools = await mcp_client.get_tools()
    return tools


def get_mcp_tools():
    return MCP_TOOLS
