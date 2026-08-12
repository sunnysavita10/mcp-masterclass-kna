import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()  # Load environment variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
        api_key=os.environ["OPENAI_API_KEY"],
        use_responses_api=True,
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

    content = result["messages"][-1].content
    if isinstance(content, list):
        content = "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    print(content)


if __name__ == "__main__":
    asyncio.run(main())
