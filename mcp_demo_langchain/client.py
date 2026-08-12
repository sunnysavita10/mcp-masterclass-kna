import asyncio
import os
import sys
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from pathlib import Path

SERVER_FILE = Path(__file__).with_name("server.py")

async def main():

    # ========================================================
    # 1. CONNECT TO MCP SERVER
    # ========================================================

    mcp_client = MultiServerMCPClient(
        {
            "travel": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(SERVER_FILE)],
            }
        }
    )


    # ========================================================
    # 2. LOAD MCP TOOLS
    # ========================================================

    tools = await mcp_client.get_tools()

    print("Available MCP Tools:")

    for tool in tools:
        print("-", tool.name)


    # ========================================================
    # 3. CREATE LLM
    # ========================================================

    model = ChatOpenAI(
        model="gpt-5.6",
        api_key=os.environ["OPENAI_API_KEY"]
    )


    # ========================================================
    # 4. CREATE LANGCHAIN AGENT
    # ========================================================

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful travel assistant. "
            "Use the available MCP tools whenever needed."
        )
    )


    # ========================================================
    # 5. ASK USER QUESTION
    # ========================================================

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content":
                        "Find me a flight from Bangalore to Dubai."
                }
            ]
        }
    )


    # ========================================================
    # 6. PRINT FINAL ANSWER
    # ========================================================

    print("\nFINAL ANSWER:")

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())