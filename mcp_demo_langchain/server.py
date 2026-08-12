from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Travel MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def search_flights(
    origin: str,
    destination: str
) -> str:
    """Search available flights between two cities."""

    return (
        f"Available flights found from {origin} to {destination}. "
        f"Flight EK501 costs ₹28,000."
    )


@mcp.tool()
def book_hotel(
    city: str,
    nights: int
) -> str:
    """Book a hotel in a city."""

    return f"Hotel booked in {city} for {nights} nights."


@mcp.resource("travel://preferences")
def travel_preferences() -> str:
    """Return travel preferences."""

    return """
Preferred airline: Emirates
Preferred seat: Window
Preferred class: Economy
Preferred hotel: 4 Star
"""


@mcp.resource("weather://{city}")
def weather(city: str) -> str:
    """Return weather information."""

    return f"Weather in {city}: Sunny, 28°C"


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


if __name__ == "__main__":
    mcp.run(transport="stdio")
