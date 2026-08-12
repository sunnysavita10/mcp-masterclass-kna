import asyncio
import json
import sys

from openai import AsyncOpenAI

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")  # Ensure the Open

# ============================================================
# OPENAI CLIENT
# ============================================================

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)  # Replace with your actual OpenAI API key

# ============================================================
# CONVERT MCP TOOL -> OPENAI TOOL
# ============================================================

def convert_mcp_tools_to_openai(mcp_tools):

    openai_tools = []

    for tool in mcp_tools:

        openai_tools.append(
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema,
            }
        )

    return openai_tools


# ============================================================
# CONVERT MCP RESULT -> TEXT
# ============================================================

def mcp_result_to_text(result):

    texts = []

    for block in result.content:

        if isinstance(block, TextContent):
            texts.append(block.text)

    return "\n".join(texts)


# ============================================================
# MAIN
# ============================================================

async def main():

    # --------------------------------------------------------
    # Start MCP Server
    # --------------------------------------------------------

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]
    )
    
    print("Starting MCP Server...")
    print(server_params)
    print(server_params.command, " ".join(server_params.args))


    # --------------------------------------------------------
    # Connect MCP Client
    # --------------------------------------------------------

    async with Client(stdio_client(server_params)) as mcp_client:

        print("Connected to MCP Server")


        # ----------------------------------------------------
        # 1. Discover MCP Tools
        # ----------------------------------------------------

        tools_result = await mcp_client.list_tools()

        print("\nMCP Tools:")

        for tool in tools_result.tools:
            print("-", tool.name)


        # ----------------------------------------------------
        # 2. Convert MCP tools into LLM tools
        # ----------------------------------------------------

        openai_tools = convert_mcp_tools_to_openai(
            tools_result.tools
        )


        # ----------------------------------------------------
        # 3. User Question
        # ----------------------------------------------------

        user_question = (
            "Find me a flight from Bangalore to Dubai."
        )

        print("\nUSER:")
        print(user_question)


        conversation = [
            {
                "role": "user",
                "content": user_question
            }
        ]


        # ----------------------------------------------------
        # 4. Ask LLM
        # ----------------------------------------------------

        response = await openai_client.responses.create(
            model="gpt-5.6",
            input=conversation,
            tools=openai_tools
        )


        # Keep model response
        conversation += response.output


        # ----------------------------------------------------
        # 5. Check whether LLM selected an MCP Tool
        # ----------------------------------------------------

        for item in response.output:

            if item.type != "function_call":
                continue


            tool_name = item.name

            arguments = json.loads(
                item.arguments
            )


            print("\nLLM DECIDED TO CALL:")
            print(tool_name)

            print("\nARGUMENTS:")
            print(arguments)


            # ------------------------------------------------
            # 6. Call actual MCP Tool
            # ------------------------------------------------

            tool_result = await mcp_client.call_tool(
                tool_name,
                arguments
            )


            tool_output = mcp_result_to_text(
                tool_result
            )


            print("\nMCP TOOL RESULT:")
            print(tool_output)


            # ------------------------------------------------
            # 7. Send MCP result back to LLM
            # ------------------------------------------------

            conversation.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": tool_output
                }
            )


        # ----------------------------------------------------
        # 8. Ask LLM for Final Answer
        # ----------------------------------------------------

        final_response = await openai_client.responses.create(
            model="gpt-5.6",
            input=conversation,
            tools=openai_tools
        )


        print("\nLLM FINAL ANSWER:")
        print(final_response.output_text)


if __name__ == "__main__":
    asyncio.run(main())