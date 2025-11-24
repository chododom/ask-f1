from typing import List, Optional

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from ask_f1_agent.config import CFG


class F1MCPClient:
    def __init__(self):
        self.client: Optional[MultiServerMCPClient] = None
        self._tools: Optional[List[BaseTool]] = []

    async def connect(self):
        """
        Connects to the MCP server using langchain-mcp-adapters.
        This automatically handles the Stdio connection and tool conversion.
        """

        # Initialize the MultiServer client
        self.client = MultiServerMCPClient(
            {
                "fastf1": {
                    "url": CFG.mcp_url,
                    "transport": "streamable_http",
                }
            }
        )

        # Get LangChain-ready tools directly
        self._tools = await self.client.get_tools()

        print(f"✅ Connected to MCP Server via Adapter. Loaded {len(self._tools)} tools.")

    @property
    def tools(self) -> List[BaseTool]:
        return self._tools

    async def disconnect(self):
        """Cleanly close the connection."""
        if self.client:
            self.client = None
            print("🔌 Disconnected from MCP Server.")


# Singleton instance to be shared across the app
mcp_manager = F1MCPClient()
