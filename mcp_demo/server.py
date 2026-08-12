from mcp.server import MCPServer

mcp = MCPServer("Travel Server")

@mcp.tool()
def my_tool():
    pass


@mcp.resource()
def my_resource():
    pass


@mcp.prompt()
def my_prompt():    
    pass
