import asyncio
import json
import sys
import os
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")  # Ensure the Open

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)  # Replace with your actual OpenAI API key

def convert_mcp_toops_to_openai(mcp_tools):
    pass

def mcp_result_to_text(result):
    pass


async def main():
    pass