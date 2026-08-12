from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Travel MCP Server")


# ============================================================
# TOOLS
# ============================================================

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def search_flights(
    origin: str,
    destination: str
) -> str:
    """Search available flights."""

    return (
        f"Available flights found "
        f"from {origin} to {destination}"
    )


@mcp.tool()
def book_hotel(
    city: str,
    nights: int
) -> str:
    """Book a hotel."""

    return (
        f"Hotel booked in {city} "
        f"for {nights} nights."
    )


# ============================================================
# RESOURCE
# ============================================================

@mcp.resource("travel://preferences")
def travel_preferences() -> str:
    """Return travel preferences."""

    return """
Preferred airline: Emirates
Preferred seat: Window
Preferred class: Economy
Preferred hotel: 4 Star
"""


# ============================================================
# RESOURCE TEMPLATE
# ============================================================

@mcp.resource("weather://{city}")
def weather(city: str) -> str:
    """Return weather information."""

    return f"Weather information for {city}"


# ============================================================
# PROMPT
# ============================================================

@mcp.prompt()
def plan_vacation(
    destination: str,
    days: str
) -> str:
    """Create vacation planning instructions."""

    return f"""
Plan a {days}-day vacation to {destination}.

Check:
1. Travel preferences
2. Flights
3. Weather
4. Hotel
"""


# ============================================================
# START STREAMABLE HTTP MCP SERVER
# ============================================================

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8000
    )