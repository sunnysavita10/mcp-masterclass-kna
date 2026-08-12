import asyncio

from mcp import Client
from mcp.types import TextContent


async def main():

    # ========================================================
    # CONNECT TO REMOTE / HTTP MCP SERVER
    # ========================================================

    async with Client(
        "http://127.0.0.1:8000/mcp"
    ) as client:

        print("Connected to MCP Server")

        print("Protocol Version:")
        print(client.protocol_version)

        print("\nServer:")
        print(client.server_info)


        # ====================================================
        # DISCOVER TOOLS
        # ====================================================

        tools_result = await client.list_tools()

        print("\nAvailable Tools:")

        for tool in tools_result.tools:
            print("-", tool.name)


        # ====================================================
        # CALL TOOL
        # ====================================================

        print("\nCalling search_flights...")

        result = await client.call_tool(
            "search_flights",
            {
                "origin": "Bangalore",
                "destination": "Dubai"
            }
        )


        print("\nTool Result:")

        for block in result.content:

            if isinstance(block, TextContent):
                print(block.text)


if __name__ == "__main__":
    asyncio.run(main())